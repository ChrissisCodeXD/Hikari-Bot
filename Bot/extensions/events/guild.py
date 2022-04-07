import hikari

from imports import *
import utils
from Bot import Logger

from Bot.DataBase.mutesys import DBMute

guild_plugin = lightbulb.Plugin("guild_events_plugin")

Log = Logger()


@guild_plugin.listener(hikari.GuildJoinEvent)
async def on_guild_join(event: hikari.GuildJoinEvent):
    #await Log.send_guild_join(event.guild)
    pass


@guild_plugin.listener(hikari.RoleDeleteEvent)
async def on_roles_delete(event: hikari.RoleDeleteEvent):
    mute_roles = DBMute(event.app.db).get_mute_roles()
    if str(event.role_id) in mute_roles:
        print("yes")


def load(bot):
    bot.add_plugin(guild_plugin)


def unload(bot):
    bot.remove_plugin(guild_plugin)
