import hikari
import lightbulb

from imports import *
from Bot.DataBase.logChannel import DBlog

log_plugin = lightbulb.Plugin("server_managment.logs")

log_plugin.add_checks(
    lightbulb.checks.guild_only
)



@log_plugin.command()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("logs","the logging system")
@lightbulb.implements(lightbulb.PrefixCommandGroup,lightbulb.SlashCommandGroup)
async def logs(ctx):
    pass


types = {
    "all_logs": "all",
    "auto delete": "message_delete",
    "mod_logs": "mod_logs"
}




choices = ["all_logs","auto delete","mod_logs"]


@logs.child()
@lightbulb.option("channel","the channel you want to log the bot in",type=hikari.GuildChannel,required=True)
@lightbulb.option("type","the type of log you want to send",type=str,required=True,choices=choices)
@lightbulb.command("add","add a log channel",inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.Context):
    channel = ctx.options.channel
    type : str = ctx.options.type
    type = types[type]

    res = DBlog(ctx.app.db).add_log_channel(ctx.guild_id,type,channel.id)

    if not res:
        embed = hikari.Embed(
            title="❌ Error",
            description="The channel is already a log channel",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )

        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed,delete_after=5)
    else:
        channel = ctx.get_guild().get_channel(channel.id)
        embed = hikari.Embed(
            title="✅ Success",
            description=f"The channel {channel.mention} has been added to the log channel",
            color=utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed,delete_after=5)


@logs.child()
@lightbulb.option("channel","the channel you want to remove from the log channel",type=hikari.TextableGuildChannel,required=True)
@lightbulb.command("remove","remove a log channel",inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def remove(ctx: lightbulb.Context):
    channel = ctx.options.channel
    res = DBlog(ctx.app.db).remove_log_channel(ctx.guild_id,channel.id)

    if not res:
        embed = hikari.Embed(
            title="❌ Error",
            description="The channel is not a log channel",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )

        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed,delete_after=5)
    else:
        channel = ctx.get_guild().get_channel(channel.id)
        embed = hikari.Embed(
            title="✅ Success",
            description=f"The channel {channel.mention} has been removed from the log channel",
            color=utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed,delete_after=5)


@logs.child()
@lightbulb.command("list","list all the log channels",inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def list(ctx: lightbulb.Context):
    res = DBlog(ctx.app.db).get_dict(ctx.guild_id)
    guild = ctx.get_guild()
    if not res:
        embed = hikari.Embed(
            title="❌ Error",
            description="There are no log channels",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed,delete_after=5)
        return
    string = ""
    print(res)
    for i in res:

        if res[i] != 0:
            string += f"{guild.get_channel(res[i]).mention} for `{i}`\n"


    embed = hikari.Embed(
        title="Log Channels",
        description=string,
        color=utils.Color.green().__str__(),
        timestamp=utils.get_time()
    )
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed,delete_after=5)




@log_plugin.listener(hikari.GuildChannelDeleteEvent)
async def on_delete(event: hikari.GuildChannelDeleteEvent):
    r_id = event.channel_id
    g_id = event.guild_id
    res = DBlog(log_plugin.app.db).get_dict(g_id)
    if not res: return

    for key,value in res.items():
        if value == r_id:
            DBlog(log_plugin.app.db).remove_log_channel(g_id,r_id)




def load(bot):
    bot.add_plugin(log_plugin)


def unload(bot):
    bot.remove_plugin(log_plugin)