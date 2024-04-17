


import onlybot
import importlib

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def get_help(app_name: str) -> None:
    try:
        module = importlib.import_module(f"onlybot.apps.{app_name}.help")
        if hasattr(module, "help"):
            module.help()
        else:
            print("在 {0} 应用里没有找到帮助文件".format(app_name))
    except ImportError:
        print("没有找到 {0} 应用".format(app_name))


def main() -> None:
    # 真彩
    console = Console(color_system="truecolor")
    console.print(f"\n:rocket: [bold]onlybot {onlybot.__version__} :rocket:", justify="center")
    console.print(f"\n[i]{onlybot.__description_cn__}", justify="center")
    console.print(f"[i]{onlybot.__description_en__}", justify="center")
    console.print(f"[i]GitHub {onlybot.__repourl__}\n", justify="center")

    # 使用方法
    table = Table.grid(padding=1, pad_edge=True)
    table.add_column("Usage", no_wrap=True, justify="left", style="bold")
    console.print(
        Panel(table, border_style="bold", title="使用方法 | Usage", title_align="left")
    )

    # 应用列表
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("参数", no_wrap=True, justify="left", style="bold")
    table.add_column("描述", no_wrap=True, style="bold")
    table.add_column("状态", no_wrap=True, justify="left", style="bold")
    table.add_row(
        "douyin 或 dy",
        "- 评论，点赞，收藏，直播弹幕，刷视频，自动回复，消息转发，发布作品",
        "⏳",
    )
    table.add_row("instagram 或 ig", "- 自动化脚本对接API")
    table.add_row("twitch 或 tv", "- 自动化脚本对接API")
    table.add_row("twitter 或 x", "- 自动化脚本对接API")
    table.add_row("youtube 或 ytb", "- 自动化脚本对接API")
    table.add_row("bilibili 或 bili", "- 自动化脚本对接API")

    table.add_row(
        "f2 -d DEBUG",
        "- 记录app的调试日志到/logs下，如遇BUG提交Issue时请附带该文件并[red]删除个人敏感信息[/red]",
        "⚠",
    )
    table.add_row(
        "Issues❓", "[link=https://github.com/lkkings/OnlyBot/issues]Click Here[/]"
    ),
    table.add_row(
        "Document📕", "[link=]Click Here[/]"
    )
    console.print(
        Panel(
            table,
            border_style="bold",
            title="应用 | apps",
            title_align="left",
            subtitle="欢迎提交PR适配更多网站或添加功能",
        )
    )
