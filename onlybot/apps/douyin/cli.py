import onlybot
import click
import typing

from pathlib import Path

from onlybot import helps
from onlybot.cli.cli_commands import set_cli_config
from onlybot.log.logger import logger
from onlybot.utils.common import (
    get_resource_path,
    merge_config,
)
from onlybot.utils.conf_manager import ConfigManager


def handler_help(
        ctx: click.Context,
        param: typing.Union[click.Option, click.Parameter],
        value: typing.Any,
) -> None:
    """
    处理帮助信息 (Handle help messages)

    根据提供的值显示帮助信息或退出上下文
    (Display help messages based on the provided value or exit the context)

    Args:
        ctx: click的上下文对象 (Click's context object).
        param: 提供的参数或选项 (The provided parameter or option).
        value: 参数或选项的值 (The value of the parameter or option).
    """

    if not value or ctx.resilient_parsing:
        return
    helps.get_help("douyin")
    ctx.exit()


@click.command(name="douyin", help="抖音机器人")
@click.option(
    "--config",
    "-c",
    type=click.Path(file_okay=True, dir_okay=False, readable=True),  # exists=True
    help="配置文件的路径，最低优先",
)
@click.option(
    "-h",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    help="显示富文本帮助",
    callback=handler_help,
)
@click.pass_context
def douyin(ctx: click.Context, config: str, cmd, **kwargs):
    # 读取低频主配置文件
    main_manager = ConfigManager(onlybot.APP_CONFIG_FILE_PATH)
    main_conf_path = get_resource_path(onlybot.APP_CONFIG_FILE_PATH)
    main_conf = main_manager.get_config("douyin")

    # 读取onlybot低频配置文件
    onlybot_manager = ConfigManager(onlybot.ONLY_BOT_CONFIG_FILE_PATH)
    onlybot_conf = onlybot_manager.get_config("onlybot")
    # 读取自定义配置文件
    if config:
        custom_manager = ConfigManager(config)
    else:
        custom_manager = main_manager
        config = main_conf_path

    custom_conf = custom_manager.get_config("douyin")
    kwargs = merge_config(main_conf, onlybot_conf, **kwargs)

    logger.info("主配置路径：{0}".format(main_conf_path))
    logger.info("自定义配置路径：{0}".format(Path.cwd() / config))
    logger.debug("主配置参数：{0}".format(main_conf))
    logger.debug("自定义配置参数：{0}".format(custom_conf))
    logger.debug("CLI参数：{0}".format(kwargs))
    kwargs["app_name"] = "douyin"
    ctx.invoke(set_cli_config, **kwargs)
