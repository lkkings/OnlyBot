from onlybot.cli.cli_console import RichConsoleManager

exception_console = RichConsoleManager().exception_console


class CommonError(Exception):

    def __init__(self, message):
        exception_console.print("ERROR")
        super().__init__(message)

    def __str__(self):
        return f"{super().__str__()}"


class JSONDecodeError(CommonError):

    def __init__(self, message=None):
        super().__init__(message)


class UnKnownError(CommonError):

    def __init__(self, message=None):
        super().__init__(message)
