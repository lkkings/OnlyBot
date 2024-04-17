import json
from concurrent.futures import CancelledError
from functools import partial
import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError

from onlybot.apps.douyin.bot import DouyinBot
from onlybot.bot.base_bot import BaseBot
from onlybot.log.logger import logger
from onlybot.utils.common import get_host_and_port_from_ws

_websocket_channel = None


async def channel(message):
    if not _websocket_channel:
        logger.error("未连接指令通道！")
    else:
        await _websocket_channel.send(message)


async def handler(websocket, path, bot: BaseBot):
    global _websocket_channel
    _websocket_channel = websocket
    logger.info(f"机器人指令通道连接成功！")
    try:
        async for message in websocket:
            # 接收客户端发送的消息，并原样返回
            try:
                _task_desc = json.loads(message)
                if _task_desc["action"] == "add_task":
                    _task_id = bot.do(_task_desc)
                    await websocket.send(json.dumps({"action": "add_task", "task_id": _task_id}))
                elif _task_desc["action"] == "del_task":
                    bot.undo(_task_desc["task_id"])

            except json.JSONDecodeError as e:
                logger.error(f"JSON 解析数据失败 {message}")
            except Exception as e:
                logger.error(f"未知异常 {e}")
    except ConnectionClosedError:
        logger.error("websocket 断开连接")
        _websocket_channel = None
    except CancelledError:
        logger.error("websocket 服务关闭")


async def main(kwargs):
    bot = DouyinBot(kwargs)
    bot.start()
    # 启动 WebSocket 服务器
    host, port = get_host_and_port_from_ws(kwargs["ws"])
    callback = partial(handler, bot=bot)
    async with websockets.serve(callback, host, port):
        logger.info(f"websocket正向连接地址: {kwargs['ws']}")
        await asyncio.Future()  # 永久等待，直到服务器关闭
