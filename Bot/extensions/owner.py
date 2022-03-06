import lightbulb

from imports import *
from Bot.DataBase.mutesys import DBMute

owner_plugin = lightbulb.Plugin("owner.owner_plugin")
owner_plugin.add_checks(
    lightbulb.checks.guild_only,
    lightbulb.checks.owner_only
)
log = logging.getLogger(__name__)
from Bot import __beta__



@owner_plugin.command()
@lightbulb.command("shutdown", "Shutds down the Bot.",guilds=[948904191559077888])
@lightbulb.implements(lightbulb.SlashCommand)
async def mute(ctx: lightbulb.Context) -> None:
    log.info("Shutdown signal received")
    await ctx.respond("Now shutting down.",flags=hikari.MessageFlag.EPHEMERAL)
    await ctx.bot.close()






def load(bot):
    bot.add_plugin(owner_plugin)


def unload(bot):
    bot.remove_plugin(owner_plugin)