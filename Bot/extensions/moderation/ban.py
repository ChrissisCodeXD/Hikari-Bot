from imports import *


ban_plugin = lightbulb.Plugin("moderation.ban")


ban_plugin.add_checks(
    lightbulb.checks.guild_only,
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.BAN_MEMBERS),
    lightbulb.checks.has_guild_permissions(hikari.Permissions.BAN_MEMBERS),
)


@ban_plugin.command()
@lightbulb.option("reason", "The Reason for kicking the Member", str, required=False)
@lightbulb.option("member", "Kicks the given Member", hikari.Member, required=True)
@lightbulb.command("ban", "Kicks the given Member")
@lightbulb.implements(lightbulb.UserCommand, lightbulb.SlashCommand, lightbulb.PrefixCommand, lightbulb.MessageCommand)
async def ban(ctx: lightbulb.Context) -> None:
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
    await ban_member(user,ctx.get_guild(),res)
    if not flags:
        await ctx.respond(f"Banning **{user}**")

    if not flags:
        await ctx.edit_last_response(f"Succesfully banned `{user}` for `{res}`!")
    else:
        await ctx.respond(f"Succesfully banned `{user}` for `{res}`!",flags=flags[0])


async def ban_member(user,guild,res):
    await ban_plugin.bot.rest.ban_member(user=user, guild=guild, reason=res)

def load(bot):
    bot.add_plugin(ban_plugin)


def unload(bot):
    bot.remove_plugin(ban_plugin)