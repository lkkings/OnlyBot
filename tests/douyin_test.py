import asyncio
import importlib

from onlybot.apps.douyin.bot import DouyinBot

kwargs = {
    "diver_type": "chrome",
    "executable_path": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "headless": False,
    "user_data_dir": r'D:\Project\OnlyBot\data\test',
    "proxy": None,
    "no_login": False
}

importlib.import_module(f"onlybot.apps.douyin.command")


def test_login():
    bot = DouyinBot(kwargs)
    bot.start()
    bot.join()


def test_comment():
    bot = DouyinBot(kwargs)
    bot.start()

    bot.do({
        "command": "dy.comment",
        "action": "add_task",
        "modal_id": "7340165930233695551",
        "message": "哈哈哈"
    })

    bot.join()


def test_like():
    bot = DouyinBot(kwargs)
    bot.start()

    bot.do({
        "command": "dy.like",
        "action": "add_task",
        "modal_id": "7340165930233695551",
    })

    bot.join()


def test_collect():
    bot = DouyinBot(kwargs)
    bot.start()

    bot.do({
        "command": "dy.collect",
        "action": "add_task",
        "modal_id": "7340165930233695551",
    })

    bot.join()


def test_auto_collect():
    bot = DouyinBot(kwargs)
    bot.start()

    bot.do({
        "command": "dy.auto_collect",
        "action": "add_task",
        "modal_id": "7340165930233695551",
    })

    bot.join()


def test_auto_like_collect_comment():
    bot = DouyinBot(kwargs)
    bot.start()
    bot.do({
        "command": "dy.auto_like_collect_comment",
        "action": "add_task",
        "modal_id": "7340530531660074292",
        "rules": [{
            "tag": "测试", "url": "", "prompt": "你好",
        }, {
            "tag": "测试1", "url": "", "prompt": "你好1",
        }, {
            "tag": "测试2", "url": "", "prompt": "你好2",
        }]
    })

    bot.join()


def test_start_live_barrage_listener():
    bot = DouyinBot(kwargs)
    bot.start()

    bot.do({
        "command": "dy.start_live_barrage_listener",
        "action": "add_task",
        "live_id": "434865499275",
    })
    bot.join()


def test_send_live_barrage():
    bot = DouyinBot(kwargs)
    bot.start()
    for i in range(5):
        bot.do({
            "command": "dy.send_live_barrage",
            "action": "add_task",
            "live_id": "434865499275",
            "message": "你好呀"
        })
    bot.join()


def test_close_live_barrage():
    bot = DouyinBot(kwargs)
    bot.start()
    bot.do({
        "command": "dy.close_live_barrage",
        "action": "add_task"
    })
    bot.join()


if __name__ == '__main__':
    pass
