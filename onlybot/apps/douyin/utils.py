import re

from onlybot.apps.douyin.element import DouyinEleSelector


async def check_is_not_login(page):
    # 使用 query_selector() 方法查找页面中是否存在文字为 "登录" 的按钮
    login_button = await page.query_selector(DouyinEleSelector.IS_LOGIN_SIGN)
    return login_button is not None





