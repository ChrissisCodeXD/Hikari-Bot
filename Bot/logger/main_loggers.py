import datetime, pytz, discord, traceback, aiohttp, time, hikari
import typing as t

import lightbulb
from discord import AsyncWebhookAdapter, Webhook
from utils.time_wrapper import class_time_wrapper
from utils.guild_icon import guild_icon


class Logger():

    def __init__(self):
        self.pytz = pytz.timezone('Europe/Berlin')
        self.time = datetime.datetime.now(tz=self.pytz)

    @class_time_wrapper
    async def send_error_log(self, err, cmd,id):
        embed = discord.Embed(
            title=f"Ein Fehler ist aufgetreten! {type(err)}",
            description=err,
            color=discord.Colour.red(),
            timestamp=self.time,
        )
        embed.add_field(name="Command:", value=f"{cmd}")
        embed.add_field(name=f"Error:", value=f"{err}")
        if id:
            embed.add_field(name=f"ID:",value=str(id))
        trc_list = [i for i in traceback.TracebackException.from_exception(err).format()]
        filename = f'./extensions/err_logs/errorlog_{cmd}_{int(time.time())}.txt'
        with open(filename, 'w') as file:
            for i in trc_list:
                file.write(i)
        file = discord.File(filename)

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                'https://discord.com/api/webhooks/948907518179033150/ZPaTOsnOpjDg04LAYs-R0RuwgjU8DEdtZjuSR8gFDdynGSflb1DdrB6AmtwMLoQAkEv5',
                adapter=AsyncWebhookAdapter(session))

            await webhook.send(
                username='Error-Log',
                avatar_url="https://cdn-icons.flaticon.com/png/512/1008/premium/1008930.png?token=exp=1646310482~hmac=2727aa6e1ff8277825b326f620dc790f",
                embed=embed,
                file=file,
            )

    @class_time_wrapper
    async def send_guild_join(self, guild: hikari.GatewayGuild):
        embed = discord.Embed(
            title=f"Bot ist einer Guild beigetreten! {guild.name}",
            color=discord.Colour.green(),
            timestamp=self.time,
        )
        embed.add_field(name="Members:", value=f"{guild.member_count}")
        embed.add_field(name=f"Guild ID:", value=f"{guild.id}")
        embed.add_field(name=f"Guild Icon hash:", value=f"{guild.icon_hash}")
        embed.set_image(url=guild_icon(guild))

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                'https://discord.com/api/webhooks/948944824357249054/VtpbLMKzFVgQf41OyXxMfaGgM28VbV8JMdlLx-ILQuheNFp1eiVb83snM-usBiKtCfJd',
                adapter=AsyncWebhookAdapter(session))

            await webhook.send(
                username='Guild-Log',
                avatar_url="https://cdn-icons.flaticon.com/png/512/2163/premium/2163271.png?token=exp=1646317406~hmac=435f9ab9a4b08285d23c342b6fbcbf30",
                embed=embed,
            )

    @class_time_wrapper
    async def send_on_start(self, bot: lightbulb.BotApp):
        embed = discord.Embed(
            title=f"Bot ist gestartet!",
            color=discord.Colour.green(),
            timestamp=self.time,
        )
        embed.add_field(name="Members:", value=f"{len(bot.cache.get_members_view())}")
        embed.add_field(name=f"Guilds:", value=f"{len(bot.cache.get_available_guilds_view())}")
        embed.add_field(name=f"Ping:", value=f"{bot.heartbeat_latency}")
        embed.set_image(url=bot.application.make_icon_url())

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                'https://discord.com/api/webhooks/950057704381100062/5L-dLg13izd4gXEMF-m1B8GYapxlhv4clKvKFstkqcjhhnZD6Zf_ZPIFRRsk9JVoaJGY',
                adapter=AsyncWebhookAdapter(session))
            await webhook.send(
                username='Info-Log',
                avatar_url="https://cdn-icons.flaticon.com/png/512/2163/premium/2163271.png?token=exp=1646317406~hmac=435f9ab9a4b08285d23c342b6fbcbf30",
                embed=embed,
            )

