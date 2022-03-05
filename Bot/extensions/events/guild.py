import hikari

from imports import *
import utils
from Bot import __prefix__, Logger

guild_plugin = lightbulb.Plugin("guild_events_plugin")

Log = Logger()


@guild_plugin.listener(hikari.GuildJoinEvent)
async def on_guild_join(event: hikari.GuildJoinEvent):
    await Log.send_guild_join(event.guild)


def load(bot):
    bot.add_plugin(guild_plugin)


def unload(bot):
    bot.remove_plugin(guild_plugin)
