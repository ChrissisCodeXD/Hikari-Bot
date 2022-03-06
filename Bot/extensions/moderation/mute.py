import lightbulb

from imports import *
from Bot.DataBase.mutesys import DBMute

mute_plugin = lightbulb.Plugin("moderation.mute_plugin")
mute_plugin.add_checks(
    lightbulb.checks.guild_only,
    lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)








async def _check(ctx: lightbulb.Context):
    result = DBMute(ctx.app.db).get_settings(ctx.guild_id)
    role = None
    mute_perms = (
            hikari.Permissions.SEND_MESSAGES
            | hikari.Permissions.SPEAK
            | hikari.Permissions.SEND_MESSAGES_IN_THREADS
    )
    if not result:
        embed = hikari.Embed(
            title="Setting up the Mute System for the first Time.",
            description=f"Could take some while.",
            color=utils.Color.magenta().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            print("a")
            await ctx.respond(embed=embed,flags=hikari.MessageFlag.EPHEMERAL)
        else:
            print("e")
            await ctx.respond(embed=embed)
        role = await ctx.app.rest.create_role(
            guild = ctx.get_guild(),
            name = "Muted",
            mentionable=False,
            reason=f"Setting up the Mute System"
        )
        guild = await ctx.get_guild().fetch_self()

        for i in guild.get_channels():
            if not type(i) == hikari.GuildChannel: i = guild.get_channel(i)
            await i.edit_overwrite(
                target = role,
                deny = mute_perms,
                reason=f"Setting up the Mute System"
            )
        DBMute(ctx.app.db).add_settings(guild.id,role.id)
        embed = hikari.Embed(
            title="Finished setting up the Mute system.",
            color=utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed,flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.edit_last_response(embed=embed,delete_after=5)
    guild = await ctx.get_guild().fetch_self()
    result = DBMute(ctx.app.db).get_settings(guild.id)
    mute_role_id = result[str(guild.id)]
    for i in guild.get_channels():
        if not type(i) == hikari.GuildChannel: i = guild.get_channel(i)
        overwrites = {}
        for e in i.permission_overwrites:
            overwrites[str(int(e))] = i.permission_overwrites[e]
        if not str(mute_role_id) in overwrites:
            if not role: role = guild.get_role(mute_role_id)
            await i.edit_overwrite(
                target=role,
                deny=mute_perms,
                reason=f"Setting up the Mute System"
            )





@mute_plugin.command()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("reason", "The Reason for kicking the Member", str, required=False)
@lightbulb.option("duration","How log the Member should be muted",str)
@lightbulb.option("member", "The Member you want to mute", hikari.Member, required=True)
@lightbulb.command("mute", "Mutes the given Member")
@lightbulb.implements(lightbulb.UserCommand, lightbulb.SlashCommand, lightbulb.PrefixCommand, lightbulb.MessageCommand)
async def mute(ctx: lightbulb.Context) -> None:
    await _check(ctx)
    #TODO finish command
    await ctx.respond("Finished!")

def load(bot):
    bot.add_plugin(mute_plugin)


def unload(bot):
    bot.remove_plugin(mute_plugin)