import hikari
import lightbulb.checks

from imports import *

kick_plugin = lightbulb.Plugin("moderation.kick")
kick_plugin.add_checks(
    lightbulb.checks.guild_only,
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.KICK_MEMBERS),
    lightbulb.checks.has_guild_permissions(hikari.Permissions.KICK_MEMBERS),
)


@kick_plugin.command()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("reason", "The Reason for kicking the Member", str, required=False)
@lightbulb.option("member", "Kicks the given Member", hikari.Member, required=True)
@lightbulb.command("kick", "Kicks the given Member")
@lightbulb.implements(lightbulb.UserCommand, lightbulb.SlashCommand, lightbulb.PrefixCommand, lightbulb.MessageCommand)
async def kick(ctx: lightbulb.Context) -> None:
    if type(ctx) == lightbulb.context.UserContext:
        user = ctx.options.target
    elif type(ctx) == lightbulb.context.MessageContext:
        user = ctx.options.target.author
    else:
        user = ctx.options.member
    flags = []
    if ctx.interaction:
        flags.append(hikari.MessageFlag.EPHEMERAL)
    res = ctx.options.reason or f"'No Reason Provided.' By {ctx.author}"

    if not flags:
        await ctx.respond(f"Kicking **{user}**")
    await kick_member(user, ctx.get_guild(), res)
    if not flags:
        await ctx.edit_last_response(f"Succesfully kicked `{user}` for `{res}`!")
    else:
        await ctx.respond(f"Succesfully kicked `{user}` for `{res}`!", flags=flags[0])


async def kick_member(user, guild, res):
    await kick_plugin.bot.rest.kick_member(user=user, guild=guild, reason=res)


def load(bot):
    bot.add_plugin(kick_plugin)


def unload(bot):
    bot.remove_plugin(kick_plugin)
