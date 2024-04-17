import asyncio
import os
import time

from playwright.async_api import Page
from playwright.sync_api import TimeoutError

import onlybot


async def use_stealth_plug(page):
    package_path = os.path.dirname(onlybot.__file__)
    js_path = os.path.join(package_path, "js", "stealth.min.js")
    await page.add_init_script(path=js_path)


async def wait_for_any_selector(page, selectors, timeout=30) -> set:
    start_time = time.time()
    while time.time() - start_time < timeout:
        all_selector = set()
        for selector in selectors:
            ele = await page.query_selector(selector)
            if not ele:
                await asyncio.sleep(0.1)
                continue
            all_selector.add(selector)
        if len(all_selector) > 0:
            return all_selector
    # 如果超时，则抛出 TimeoutError
    raise TimeoutError(f"Timeout occurred while waiting for any of the selectors: {selectors}")


async def click(page: Page, selector: str):
    await page.wait_for_selector(selector)
    ele = await page.query_selector(selector)
    await ele.click()


async def goto(page: Page, url: str):
    if url not in page.url:
        await page.goto(url)
        await page.wait_for_load_state()


async def press(page: Page, key: str, is_key=True):
    if is_key:
        await page.keyboard.press(key)
    else:
        await page.keyboard.insert_text(key)


async def wheel(page: Page, x=0, y=0):
    await page.mouse.wheel(delta_y=y, delta_x=x)


async def center(page: Page):
    # 获取页面的尺寸
    width, height = await page.evaluate('''() => {
             return [document.body.clientWidth, document.body.clientHeight];
         }''')

    # 计算页面中心坐标
    center_x = width / 2
    center_y = height / 2

    # 在页面中心位置模拟鼠标点击
    await page.mouse.click(center_x, center_y)
