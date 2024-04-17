from onlybot.log.logger import logger

command_map = {}


def command(name):
    def decorator(func):
        logger.debug(f"检测到指令{name}")
        command_map[name] = func

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
