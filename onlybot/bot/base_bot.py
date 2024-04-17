import asyncio
import queue
import threading
import time
import traceback
from concurrent.futures import CancelledError
from typing import List

from playwright.async_api import Page, BrowserContext

from onlybot.browser import BrowserDriver
from onlybot.log.logger import logger
from onlybot.utils.command import command_map
from onlybot.utils.driver_utils import use_stealth_plug


class BaseBot(threading.Thread):

    def __init__(self, kwargs):
        super().__init__()
        self.init_url = "https://www.baidu.com"
        self._page_map = {}
        self._request_map = {}
        self._response_map = {}
        self.browser: BrowserContext = None
        self.running = False
        self.kwargs = kwargs
        self.pending_task_queue = queue.SimpleQueue()
        self._current_exec_task = None
        self._current_exec_task_id = -1
        self._counter = 0

    @property
    def driver(self):
        kwargs = self.kwargs
        diver_type = kwargs.get("diver_type")
        executable_path = kwargs.get("executable_path")
        headless = kwargs.get("headless")
        user_data_dir = kwargs.get("user_data_dir")
        proxy = kwargs.get("proxy")
        if proxy:
            username_password, proxy_server = proxy.split("@", 1)
            username, password = username_password.split(":", 1)
            proxy = {
                'server': proxy_server,
                'username': username,
                'password': password
            }
        return BrowserDriver(driver_type=diver_type,
                             executable_path=executable_path,
                             headless=headless,
                             proxy=proxy,
                             user_data_dir=user_data_dir)

    async def _request_handler(self, request, page_name):
        func_list = self._request_map[page_name]
        for func in func_list:
            if func:
                await func(request)

    async def _bind_on_request(self, page_name: str):
        _page = self._page_map[page_name]
        _page.on("request", lambda request: self._request_handler(request, page_name))
        logger.debug(f"name: {page_name} page: {_page.url} 绑定请求监听")

    async def create_page(self, page_name: str, page: Page = None, use_stealth=True) -> Page:
        if self._page_map.get(page_name):
            return self._page_map[page_name]
        if not page:
            page = await self.browser.new_page()
        if use_stealth:
            await use_stealth_plug(page)
        self._page_map[page_name] = page
        self._request_map[page_name] = []
        await self._bind_on_request(page_name)
        return page

    async def close_page(self, page_name: str) -> Page:
        _page = self._page_map[page_name]
        await _page.close()
        del self._page_map[page_name]
        del self._request_map[page_name]
        return _page

    async def get_page(self, page_name="init") -> Page:
        if not self._page_map.get(page_name):
            return self._page_map["init"]
        else:
            return self._page_map[page_name]

    def add_on_request_handler_for_one_page(self, page_name="init", callback=None):
        if not self._page_map.get(page_name):
            self._request_map["init"].append(callback)
        else:
            self._request_map[page_name].append(callback)
        logger.info(f"{page_name} 添加监听 {callback.__name__}")

    def remove_on_request_handler_for_one_page(self, page_name, callback):
        if not self._page_map.get(page_name):
            self._request_map["init"].remove(callback)
        else:
            self._request_map[page_name].remove(callback)

    def add_on_request_handler_for_all_page(self, callback):
        for page_name, _ in self._page_map:
            self.add_on_request_handler_for_one_page(page_name, callback)

    def remove_on_request_handler_for_all_page(self, callback):
        for page_name, _ in self._page_map:
            self.remove_on_request_handler_for_one_page(page_name, callback)

    async def _init_bot(self):
        browser = await self.driver.launch()
        self.browser = browser
        page = self.browser.pages[0]
        await self.create_page("init", page)
        await page.wait_for_load_state()
        await page.goto(self.init_url)
        if not self.kwargs.get("no_login"):
            await self.login(page)
        logger.info("机器人启动成功！")

    async def login(self, page: Page):
        raise NotImplementedError

    def run(self) -> None:
        self.running = True

        async def boot():
            await self._init_bot()
            await self._handler_worker()

        asyncio.run(boot())

    async def shutdown(self):
        self.running = False
        logger.info("浏览器已关闭")
        await self.driver.close()

    async def _handler_worker(self):
        while self.running:
            if not self.pending_task_queue.empty():
                try:
                    params = self.pending_task_queue.get()
                    command = params["command"]
                    task_id = params["task_id"]
                    params.pop("command")
                    params.pop("action")
                    params.pop("task_id")
                    print(f"ID {task_id} COMMAND: {command} => Params: {params}")
                    logger.debug(f"ID {task_id} COMMAND: {command} => Params: {params}")
                    if command not in command_map:
                        logger.error("未知命令!")
                        continue
                    _task_exec_fun = command_map[command]
                    self._current_exec_task_id = task_id
                    _exec_task = asyncio.create_task(_task_exec_fun(task_id, self, **params))
                    self._current_exec_task = _exec_task
                    await self._current_exec_task
                except TypeError as e:
                    logger.error(f"Error calling function {_task_exec_fun.__name__} with arguments {params}: {e}")
                except KeyError as e:
                    logger.error(f"arguments: {params} Not Found {e}!")
                except CancelledError as e:
                    logger.debug(f'task_id: {task_id} command: {command} arguments: {params} cancelled')
                finally:
                    await asyncio.sleep(0.1)
            else:
                await asyncio.sleep(1)

    def do(self, params):
        self._counter += 1
        params["task_id"] = self._counter
        self.pending_task_queue.put(params)
        return self._counter

    def undo(self, task_id):
        if self._current_exec_task_id == task_id:
            self._current_exec_task.cancel()
        else:
            temp_queue = queue.SimpleQueue()
            while not self.pending_task_queue.empty():
                params = self.pending_task_queue.get()
                if params["task_id"] != task_id:
                    temp_queue.put(params)
            while not temp_queue.empty():
                self.pending_task_queue.put(temp_queue.get())
