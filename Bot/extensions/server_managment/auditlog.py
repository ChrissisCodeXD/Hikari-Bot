import lightbulb

from imports import *


auditlog_plugin = lightbulb.Plugin("server_managment.plugin")

auditlog_plugin.add_checks(
    lightbulb.checks.guild_only,
)



async def build_rows(ctx:lightbulb.Context):
    bot = ctx.app

    settings = None




@auditlog_plugin.command()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("auditlog","The Auditlog System")
@lightbulb.implements(lightbulb.PrefixCommandGroup,lightbulb.SlashCommandGroup)
async def auditlog(ctx: lightbulb.Context):
    pass



@auditlog.child()
@lightbulb.command("settings","The Auditlog Settings")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def settings(ctx: lightbulb.Context):
    pass


def load(bot):
    bot.add_plugin(auditlog_plugin)



def unload(bot):
    bot.remove_plugin(auditlog_plugin)