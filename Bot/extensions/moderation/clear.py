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
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("messages", "Messages to delete", int, required=True)
@lightbulb.option("user", "User to delete messages from", hikari.Member, required=False)
@lightbulb.command("clear", "Clears the Current Channel")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def clear(ctx: lightbulb.Context) -> None:
    user = ctx.options.user if ctx.options.user else None
    channel: hikari.GuildTextChannel = ctx.get_channel()
    deleted = await utils.purge(channel.id, ctx.options.messages, clear_plugin.bot,user)
    if ctx.interaction:
        await ctx.respond(f"Deleted {deleted if deleted <= 100 else 100} Messages!",
                      flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(f"Deleted {deleted if deleted <= 100 else 100} Messages!",delete_after=5)


def load(bot):
    bot.add_plugin(clear_plugin)


def unload(bot):
    bot.remove_plugin(clear_plugin)
