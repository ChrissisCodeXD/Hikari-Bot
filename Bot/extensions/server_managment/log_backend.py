import hikari

from imports import *
from Bot.DataBase.logChannel import DBlog
log_backend_plugin = lightbulb.Plugin("server_managment.log_backend")



async def message_delete(guild:hikari.Guild,message:hikari.Message,reason,fields:dict=None):

    res = DBlog(log_backend_plugin.app.db).get_dict(guild.id)
    c_id = res["message_delete"]
    if c_id == 0: return
    channel = guild.get_channel(c_id)
    if not channel: return

    embed = hikari.Embed(
        title="Message Deleted",
        description=f"Message Author: {message.author.mention} | {message.author} \n"
                    f"Message Content: || {message.content} ||\n"
                    f"Message ID: {message.id}\n"
                    f"Message Channel: {guild.get_channel(message.channel_id).mention} | {guild.get_channel(message.channel_id).name}\n"
                    f"Reason: {reason}",
        timestamp=utils.get_time()
    )
    embed.set_thumbnail(message.author.make_avatar_url())
    if fields:
        for key,value in fields.items():
            embed.add_field(name=key,value=value)

    all_id = res["all_logs"]
    if all_id == 0: return
    all_channel = guild.get_channel(all_id)
    if all_channel:
        await all_logs(embed, all_channel)

    await channel.send(embed=embed)

async def audit_log(guild:hikari.Guild,fields:dict=None):
    res = DBlog(log_backend_plugin.app.db).get_dict(guild.id)
    c_id = res["audit_log"]
    if c_id == 0: return
    channel: hikari.GuildChannel = guild.get_channel(c_id)
    if not channel: return

    embed = hikari.Embed(
        title="Audit Log",
        timestamp=utils.get_time()
    )
    if fields:
        for key,value in fields.items():
            embed.add_field(name=key,value=value)

    all_id = res["all_logs"]
    if all_id == 0: return
    all_channel = guild.get_channel(all_id)
    if all_channel:
        await all_logs(embed,all_channel)

    await channel.send(embed=embed)


async def all_logs(embed,channel):
    await channel.send(embed=embed)






def load(bot):
    bot.add_plugin(log_backend_plugin)

def unload(bot):
    bot.remove_plugin(log_backend_plugin)