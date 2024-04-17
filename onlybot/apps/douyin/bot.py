import asyncio
import re
import sys

from playwright.async_api import Page

from onlybot.apps.douyin.api import DouyinAPIEndpoints
from onlybot.apps.douyin.element import DouyinEleSelector
from onlybot.apps.douyin.utils import check_is_not_login
from onlybot.bot.base_bot import BaseBot
from onlybot.cli import RichConsoleManager
from onlybot.log.logger import logger
from onlybot.utils.common import not_atodo
from onlybot.utils.driver_utils import wait_for_any_selector, click
from onlybot.utils.qrcode import show_qrcode

rich_console = RichConsoleManager().rich_console
rich_prompt = RichConsoleManager().rich_prompt


class DouyinBot(BaseBot):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.init_url = DouyinAPIEndpoints.DOUYIN_DOMAIN

    async def login(self, page: Page):
        if await check_is_not_login(page):
            await self._try_login(page)
        await click(page, DouyinEleSelector.MY_NAV_TAG)
        await page.wait_for_selector(DouyinEleSelector.LOGIN_USER_NICKNAME)
        nickname_tag = await page.query_selector(DouyinEleSelector.LOGIN_USER_NICKNAME)
        nickname = await nickname_tag.text_content()
        rich_console.print(f"当前用户: [bold blue]{nickname}[/bold blue]")

    async def __check_qrcode(self, response, login_success_event):
        if response and response.url.startswith(DouyinAPIEndpoints.SSO_LOGIN_CHECK_QR):
            status_mapping = {
                "1": {"message": "[  登录  ]:等待二维码扫描！", "log": logger.info},
                "2": {"message": "[  登录  ]:扫描二维码成功！", "log": logger.info},
                "3": {"message": "[  登录  ]:确认二维码登录！", "log": logger.info},
                "4": {"message": "[  登录  ]:访问频繁，请检查参数！", "log": logger.warning},
                "5": {"message": "[  登录  ]:二维码过期，重新获取！", "log": logger.warning, },
                "-1": {"message": "[  登录  ]:为保护你的账号安全，将使用手机验证码进行身份验证!", "log": logger.warning},
                "2046": {"messages": "[  登录  ]:扫码环境异常，请前往app验证！", "log": logger.warning},
            }
            check_response = await response.json()
            check_status = check_response["data"]["status"] if check_response.get("data") else -1
            status_info = status_mapping.get(check_status, {})
            message = status_info.get("message", "")
            log_func = status_info.get("log", logger.info)
            log_func(message)
            page = await self.get_page()
            if check_status == -1:
                await self._goto_sms_login(page)
                await self._try_sms_login(page)
            elif check_status == 5:
                show_qrcode(check_response["data"]["qrcode"])
            elif check_status == 3:
                login_success_event.set()
        if response and response.url.startswith(DouyinAPIEndpoints.SMS_LOGIN_VALIDATE):
            status_mapping = {
                "-1": {"message": "[  登录  ]:验证成功!", "log": logger.info},
                "1202": {"messages": "[  登录  ]:验证码错误，请重新输入!", "log": logger.warning},
                "1203": {"messages": "[  登录  ]:错误次数过多或验证码过期，请稍后重试", "log": logger.warning},
            }
            check_response = await response.json()
            error_code = check_response["data"].get("error_code")
            check_status = error_code if error_code else -1
            status_info = status_mapping.get(check_status, {})
            message = status_info.get("message", "")
            log_func = status_info.get("log", logger.info)
            log_func(message)
            if check_status == -1:
                login_success_event.set()
            else:
                sys.exit(0)

    async def _goto_sms_login(self, page):
        await click(page, DouyinEleSelector.RE_SMS_VERIFY_TAG)
        await click(page, DouyinEleSelector.RE_SMS_CODE_SEND_BUTTON)

    async def _try_sms_login(self, page):
        sms_code = rich_prompt.ask("[bold yellow]请输入验证码[/bold yellow]")
        await page.type(DouyinEleSelector.RE_SMS_CODE_INPUT, sms_code)
        await click(page, DouyinEleSelector.RE_SMS_CODE_SUMMIT_BUTTON)

    async def _try_login(self, page: Page):
        selector = DouyinEleSelector.LOGIN_GET_QR
        await page.wait_for_selector(selector)
        step1 = await page.query_selector(selector)
        # 获取图片元素的src属性值
        src_attribute = await step1.get_attribute('src')
        # 使用正则表达式提取base64编码部分
        base64_match = re.match(r"data:image/jpeg;base64,(.*)", src_attribute)
        base64_data = base64_match.group(1)
        show_qrcode(base64_data)
        logger.info("[  登录  ]:等待二维码扫描！")
        login_success_event = asyncio.Event()
        page.on("response",
                lambda response: self.__check_qrcode(response=response, login_success_event=login_success_event))
        await login_success_event.wait()
        await asyncio.sleep(10)
        page.on("response", lambda response: not_atodo())
