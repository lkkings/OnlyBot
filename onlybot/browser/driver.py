from playwright.async_api import async_playwright, BrowserContext
from onlybot.exceptions import DriverNotSupportedError
from playwright.async_api._generated import Playwright as SyncPlaywright


class Driver:
    CHROME = "chrome"
    FIREFOX = "firefox"


class BrowserDriver:
    p: SyncPlaywright

    def __init__(self, driver_type: str, executable_path: str, headless: bool, proxy: dict = None,
                 user_data_dir: str = None):
        self.driver_type = driver_type
        self.executable_path = executable_path
        self.headless = headless
        self.proxy = proxy
        self.user_data_dir = user_data_dir

    async def launch(self) -> BrowserContext:
        self.p = await async_playwright().start()
        if self.driver_type == Driver.CHROME:
            return await self.p.chromium.launch_persistent_context(executable_path=self.executable_path,
                                                                   headless=self.headless,
                                                                   proxy=self.proxy, user_data_dir=self.user_data_dir)
        elif self.driver_type == Driver.FIREFOX:
            return await self.p.firefox.launch_persistent_context(executable_path=self.executable_path,
                                                                  headless=self.headless,
                                                                  proxy=self.proxy, user_data_dir=self.user_data_dir)
        else:
            raise DriverNotSupportedError()

    async def close(self):
        await self.p.stop()
