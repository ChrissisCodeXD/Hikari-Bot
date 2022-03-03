import hikari
import lightbulb.checks

from imports import *

kick_plugin = lightbulb.Plugin("kick")
kick_plugin.add_checks(
    lightbulb.checks.guild_only,
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.KICK_MEMBERS),
    lightbulb.checks.has_guild_permissions(hikari.Permissions.KICK_MEMBERS),
)


@kick_plugin.command()
@lightbulb.option("member", "Kicks the given Member", hikari.Member, required=True)
@lightbulb.option("reason", "The Reason for kicking the Member", str, required=False)
@lightbulb.command("kick", "Kicks the given Member")
@lightbulb.implements(lightbulb.UserCommand, lightbulb.SlashCommand, lightbulb.PrefixSubCommand)
async def kick(ctx: lightbulb.Context) -> None:
    user = ctx.options.target if ctx.options.target else ctx.options.member
    res = ctx.options.reason or f"'No Reason Provided.' By {ctx.author.username}"
    await ctx.respond(f"Kicking **{user}**")
    await ctx.bot.rest.kick_member( guild=ctx.get_guild(), reason=res)
    await ctx.edit_last_response(f"Succesfully kicked `{user}` for `{res}`!")


def load(bot):
    bot.add_plugin(kick_plugin)


def unload(bot):
    bot.remove_plugin(kick_plugin)
