from onlybot.cli.cli_console import RichConsoleManager

exception_console = RichConsoleManager().exception_console


class DriverError(Exception):
    def __init__(self, message=None):
        exception_console.print("ERROR")
        super().__init__(message)

    def __str__(self):
        """返回错误信息和文件路径（如果有的话）"""
        return f"{super().__str__()}"


class DriverNotSupportedError(DriverError):
    """基本API异常类，其他API异常都会继承这个类"""

    def __init__(self, message=None):
        super().__init__(message)

