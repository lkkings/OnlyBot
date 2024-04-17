import asyncio
import gzip
import random
import time

import requests
from playwright.async_api import ElementHandle
from google.protobuf.json_format import MessageToJson

from onlybot.apps.douyin.api import DouyinAPIEndpoints
from onlybot.apps.douyin.bot import DouyinBot
from onlybot.apps.douyin.element import DouyinEleSelector
from onlybot.log.logger import logger
from onlybot.utils.command import command
from onlybot.apps.douyin.handler import channel
from onlybot.utils.common import match_regex
from onlybot.utils.driver_utils import click, goto, press, wheel
import onlybot.apps.douyin.proto.transport_webcast_im_pb2 as pd1
import onlybot.apps.douyin.proto.message_pb2 as pd2


@command("dy.echo")
async def echo(task_id: int, bot: DouyinBot, message: str):
    await channel(f"task_id:{task_id} message: {message}")


@command("dy.comment")
async def comment(task_id: int, bot: DouyinBot, modal_id: str, message: str):
    page = await bot.get_page()
    url = f"{DouyinAPIEndpoints.DISCOVER_URL}?modal_id={modal_id}"
    await goto(page, url)
    await click(page, DouyinEleSelector.OPEN_COMMENT_TAG)
    await click(page, DouyinEleSelector.CLICK_COMMENT_INPUT)
    await asyncio.sleep(1)
    await press(page, message, False)
    await press(page, "Enter")


@command("dy.like")
async def like(task_id: int, bot: DouyinBot, modal_id: str):
    page = await bot.get_page()
    url = f"{DouyinAPIEndpoints.DISCOVER_URL}?modal_id={modal_id}"
    await goto(page, url)
    await click(page, DouyinEleSelector.VIDEO_LIKE)


@command("dy.collect")
async def collect(task_id: int, bot: DouyinBot, modal_id: str):
    page = await bot.get_page()
    url = f"{DouyinAPIEndpoints.DISCOVER_URL}?modal_id={modal_id}"
    await goto(page, url)
    await click(page, DouyinEleSelector.VIDEO_COLLECT)


@command("dy.auto_collect")
async def auto_collect(task_id: int, bot: DouyinBot, modal_id: str, interval_ms=1000, count=float("inf")):
    page = await bot.get_page()
    url = f"{DouyinAPIEndpoints.DISCOVER_URL}?modal_id={modal_id}"
    await goto(page, url)
    i = 0
    while i < count:
        await asyncio.sleep(interval_ms // 1000)
        await press(page, "c")
        random_y = random.randint(100, 200)
        await wheel(page, y=random_y)


@command("dy.start_live_barrage_listener")
async def start_live_barrage_listener(task_id: int, bot: DouyinBot, live_id: str):
    page = await bot.create_page("live")
    url = f"{DouyinAPIEndpoints.DOUYIN_LIVE_DOMAIN}/{live_id}"
    await goto(page, url)

    async def onwebsocket(websocket):
        im = pd1.transport.webcast.im
        PushFrame = im.PushFrame()

        async def decode_message(byte):
            Response = im.Response()
            Response.ParseFromString(byte)
            for item in Response.messages:
                Message = None
                if item.method == 'WebcastMemberMessage':
                    Message = pd2.webcast_im_MemberMessage()
                if item.method == 'WebcastChatMessage':
                    Message = pd2.webcast_im_ChatMessage()
                if item.method == 'WebcastGiftMessage':
                    Message = pd2.webcast_im_GiftMessage()
                if item.method == 'WebcastSocialMessage':
                    Message = pd2.webcast_im_SocialMessage()
                if item.method == 'WebcastLikeMessage':
                    Message = pd2.webcast_im_LikeMessage()
                if item.method == 'WebcastRoomStatsMessage':
                    Message = pd2.webcast_im_RoomStatsMessage()
                if Message:
                    Message.ParseFromString(item.payload)
                    message = MessageToJson(Message)
                    logger.info(message)
                    channel(message)

        async def on_received(frame):
            try:
                PushFrame.ParseFromString(frame)
                payload = PushFrame.payload
                headers_list = {}
                for item in PushFrame.headers:
                    headers_list[item.key] = item.value
                if 'compress_type' in headers_list and headers_list['compress_type'] == 'gzip':
                    decompressed_data = gzip.decompress(payload)
                    await decode_message(decompressed_data)
                else:
                    await decode_message(payload)
            except:
                pass

        websocket.on("framereceived", on_received)

    page.on("websocket", lambda websocket: onwebsocket(websocket))


@command("dy.auto_like_collect_comment")
async def auto_like_collect_comment(task_id: int, bot: DouyinBot, modal_id: str, rules: list = None,
                                    watch_time_range=(10, 60), interval_ms=3000,
                                    auto_exec_time=3600):
    page = await bot.get_page()

    # async def _remove_robot_check(request):
    #     if request.url.startswith(DouyinAPIEndpoints.REBOT_CHECK):
    #         await page.wait_for_selector(DouyinEleSelector.PASS_CAPTCHA)
    #         _is_has_captcha = await page.query_selector(DouyinEleSelector.PASS_CAPTCHA)
    #         logger.info(page.url)
    #         if _is_has_captcha:
    #             await click(page, DouyinEleSelector.CLOSE_CAPTCHA)
    #             logger.info("关闭验证码")
    #
    # bot.add_on_request_handler_for_one_page(callback=_remove_robot_check)
    url = f"{DouyinAPIEndpoints.DISCOVER_URL}?modal_id={modal_id}"
    await goto(page, url)
    await click(page, DouyinEleSelector.OPEN_COMMENT_TAG)

    _start_time = time.time()
    _tag_list = [rule["tag"] for rule in rules]
    while time.time() - _start_time < auto_exec_time:
        await asyncio.sleep(interval_ms // 1000)
        is_live_flag = await page.locator(DouyinEleSelector.RECOMMEND_VIDEO_IS_LIVE).is_visible()
        if not is_live_flag:
            if len(_tag_list) != 0:
                _video_desc: ElementHandle = None
                _video_desc_list = await page.query_selector_all(DouyinEleSelector.VIDEO_DESC)
                if len(_video_desc_list) == 2:
                    _video_desc = _video_desc_list[0]
                elif len(_video_desc_list) == 3:
                    _video_desc = _video_desc_list[1]
                assert _video_desc is not None, "未获取到视频文案"
                account_name_tag = await _video_desc.query_selector("div.account > div.account-name")
                account_name = await account_name_tag.text_content()
                video_create_time_tag = await _video_desc.query_selector("div.account > div.video-create-time > span")
                video_create_time = await video_create_time_tag.text_content()
                video_desc_text_tag = await _video_desc.query_selector("div.title > div > div > span > span > "
                                                                       "span:nth-child(1) > span > span > span")
                video_desc_text = await video_desc_text_tag.text_content() if video_desc_text_tag else ""
                video_all_tags = await _video_desc.query_selector_all("div.title > div > div > span > span > "
                                                                      "span > a")
                _video_tag_list = [await tag.text_content() for tag in video_all_tags]
                data = {
                    "tags": _video_tag_list,
                    "account_name": account_name,
                    "create_time": video_create_time,
                    "desc": video_desc_text,
                }
                logger.info(data)
                idx = match_regex(_tag_list, _video_tag_list)
                if idx != -1:
                    watch_time = random.randint(watch_time_range[0], watch_time_range[1])
                    await asyncio.sleep(watch_time)
                    comment_generation_response = requests.post(url=rules[idx].get("url"), data=data)
                    comment_text = comment_generation_response.text
                    await click(page, DouyinEleSelector.CLICK_COMMENT_INPUT)
                    await asyncio.sleep(1)
                    await press(page, comment_text, False)
                    await press(page, "Enter")
        else:
            logger.info("该视频为直播！")
        await press(page, "c")
        await asyncio.sleep(interval_ms // 1000)
        await press(page, "z")
        await asyncio.sleep(interval_ms // 1000)
        await press(page, "s")


@command("dy.send_live_barrage")
async def send_live_barrage(task_id: int, bot: DouyinBot, live_id: str, message: str):
    page = await bot.create_page("live")
    url = f"{DouyinAPIEndpoints.DOUYIN_LIVE_DOMAIN}/{live_id}"
    await goto(page, url)
    await page.locator(DouyinEleSelector.LIVE_BARRAGE_INPUT).fill(message)
    await press(page, "Enter")


@command("dy.close_live_barrage")
async def send_live_barrage(task_id: int, bot: DouyinBot):
    await bot.close_page("live")
