import hikari
import lightbulb.checks

from imports import *

clear_plugin = lightbulb.Plugin("moderation.clear")
clear_plugin.add_checks(
    lightbulb.checks.guild_only,
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
)


@clear_plugin.command()
@lightbulb.option("messages", "Messages to delete", int, required=True)
@lightbulb.command("clear", "Clears the Current Channel")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def clear(ctx: lightbulb.Context) -> None:
    channel: hikari.GuildTextChannel = ctx.get_channel()
    await utils.purge(channel.id, ctx.options.messages, clear_plugin.bot)
    await ctx.respond(f"Deleted {ctx.options.messages if ctx.options.messages <= 100 else 100} Messages!",
                      delete_after=4)


def load(bot):
    bot.add_plugin(clear_plugin)


def unload(bot):
    bot.remove_plugin(clear_plugin)
