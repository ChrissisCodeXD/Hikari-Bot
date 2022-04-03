import lightbulb
import urllib.request
import utils
from imports import *
from lightbulb.ext import tasks
from coc import utils as cocutils
from Bot.DataBase.cocsys import DBCoc

INFO_CHANNEL_ID = 953343124825063504  # some discord channel ID
WELCOME_CHANNEL_ID = 952885037152481340
clan_tags = ["#2LQQ9Q8C9"]
INFORMATION_CHANNEL_ID = 952871676079644774
GUILD_ID = 952871675375022141
WAR_CHANNEL_ID = 952871676079644775
coc_plugin = lightbulb.Plugin("fun.coc_plugin")

coc_client = coc.login("schwarzlichtampel@gmail.com", "Disco2007!",
                       key_names="coc.py tests",
                       client=coc.EventsClient,
                       )

logging.basicConfig(level=logging.ERROR)



@coc_plugin.listener(hikari.InteractionCreateEvent)
async def on_interaction(event:hikari.InteractionCreateEvent):
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return
    else:
        event.interaction: hikari.ComponentInteraction = event.interaction
    i = event.interaction
    if not i.guild_id: return
    if not i.custom_id.startswith("accept-rules"): return

    auth: hikari.InteractionMember = event.interaction.member
    guild = event.interaction.get_guild()
    if not 952885313154482188 in auth.role_ids:
        role = guild.get_role(952885313154482188)
        await auth.add_role(role=role, reason=f"Rules Accepted")


        embed = hikari.Embed(
            title = f"✅ Accepted the Rules!",
            color=utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )

        await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE,embed=embed,flags=hikari.MessageFlag.EPHEMERAL)
    else:
        embed = hikari.Embed(
            title=f"❌ Already Accepted the Rules",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )

        await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, embed=embed,
                                        flags=hikari.MessageFlag.EPHEMERAL)




@coc_plugin.command()
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command("send_rules", "sends_rules")
@lightbulb.implements(lightbulb.PrefixCommand)
async def send_rules(ctx):
    embeds = [
        hikari.Embed(color=8572125).set_image(
            "https://cdn.discordapp.com/attachments/899676897120763914/940982201821053029/WILLKOMMEN_10.png"),
        hikari.Embed(title=f"§2 Benutzernamen",
                     color=8572125,
                     description="> :small_blue_diamond: Anstößige u. o. beleidigende, rassistische Benutzernamen sind \n> verboten.\n\n> :small_blue_diamond: Benutzernamen die berühmte Personen simulieren,\n>  sind verboten.")
            .set_image("https://cdn.discordapp.com/attachments/899676897120763914/940777404601860126/unknown.png"),
        hikari.Embed(title=f"§3 Profilbilder",
                     color=8572125,
                     description=">>> :small_blue_diamond: Rechtsextremistische, sexistische & linksextremistische Profilbilder sollten zu keinem Zeitpunkt angewendet werden! Das Team behält sich vor, solch ein Verhalten zu sanktionieren.")
            .set_image("https://cdn.discordapp.com/attachments/899676897120763914/940777404601860126/unknown.png"),
        hikari.Embed(title="§4 Verhalten",
                     color=8572125,
                     description= "> :small_blue_diamond: Sarkastische Äußerungen sollten als sarkastisch gekennzeichnet werden, damit Missverständnisse > vermieden werden können.\n\n> :small_blue_diamond: Provokante, rechts- und linksextremistische sowie beleidigende Aussagen sind nicht zu äußern!\n\n> :small_blue_diamond: Das wiederholen von Nachrichten (Spamming) ist untersagt!\n\n> :small_blue_diamond: Echtgeldhandel oder drgl. ist verboten!")
            .set_image("https://cdn.discordapp.com/attachments/899676897120763914/940777404601860126/unknown.png")
    ]
    actionrow = ctx.bot.rest.build_action_row()
    actionrow.add_button(
        hikari.messages.ButtonStyle.SUCCESS,
        "accept-rules"
    ).set_label(f"Accept").set_emoji("✅").add_to_container()
    await ctx.respond(embeds=embeds,component=actionrow)

@coc_plugin.command()
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command("send_rules2", "sends_rules")
@lightbulb.implements(lightbulb.PrefixCommand)
async def send_rules2(ctx):
    if not ctx.interaction: await ctx.event.message.delete()
    embeds = [hikari.Embed(title="Aktzeptiere die Regeln hier ⬇️",color=8572125)]
    actionrow = ctx.bot.rest.build_action_row()
    actionrow.add_button(
        hikari.messages.ButtonStyle.SUCCESS,
        "accept-rules"
    ).set_label(f"Accept").set_emoji("✅").add_to_container()
    await ctx.respond(embeds=embeds, component=actionrow)

@coc_client.event
@coc.ClanEvents.member_join(tags=clan_tags)
async def on_clan_member_join(member, clan):
    channel = await coc_plugin.app.rest.fetch_channel(WELCOME_CHANNEL_ID)
    embed = hikari.Embed(title="{0.name} ({0.tag}) just " "joined our clan {1.name} ({1.tag})!".format(member, clan),
                         color=utils.Color.random().__str__(),
                         timestamp=utils.get_time())

    embed.set_thumbnail(clan.badge.url)
    await coc_plugin.app.rest.create_message(embed=embed,
                                             channel=channel
                                             )


@coc_client.event
@coc.ClanEvents.member_name(tags=clan_tags)
async def member_name_change(old_player, new_player):
    channel = await coc_plugin.app.rest.fetch_channel(INFO_CHANNEL_ID)
    embed = hikari.Embed(
        title="Name Change! {0.name} is now called {1.name} (his tag is {1.tag})".format(old_player, new_player),
        color=utils.Color.random().__str__(),
        timestamp=utils.get_time())
    embed.set_thumbnail(old_player.clan.badge.url)
    await coc_plugin.app.rest.create_message(embed=embed,
                                             channel=channel
                                             )


@coc_client.event
@coc.ClanEvents.member_donations(tags=clan_tags)
async def on_clan_member_donation(old_member, new_member):
    final_donated_troops = new_member.donations - old_member.donations
    channel = await coc_plugin.app.rest.fetch_channel(952960285885464576)
    embed = hikari.Embed(
        title=f"{new_member} just donated {final_donated_troops} troops!",
        color=utils.Color.random().__str__(),
        timestamp=utils.get_time())
    embed.set_thumbnail(new_member.clan.badge.url)
    await coc_plugin.app.rest.create_message(embed=embed,
                                             channel=channel
                                             )


@coc_client.event
@coc.ClanEvents.points(tags=clan_tags)
async def on_clan_trophy_change(old_clan, new_clan):
    channel = await coc_plugin.app.rest.fetch_channel(INFO_CHANNEL_ID)
    embed = hikari.Embed(
        title=f"{new_clan.name} total trophies changed from {old_clan.points} to {new_clan.points}",
        color=utils.Color.random().__str__(),
        timestamp=utils.get_time())
    embed.set_thumbnail(new_clan.badge.url)
    await coc_plugin.app.rest.create_message(embed=embed,
                                             channel=channel
                                             )


@coc_client.event
@coc.ClanEvents.member_versus_trophies(tags=clan_tags)
async def clan_member_versus_trophies_changed(old_member, new_member):
    channel = await coc_plugin.app.rest.fetch_channel(INFO_CHANNEL_ID)
    embed = hikari.Embed(
        title=f"{new_member} versus trophies changed from {old_member.versus_trophies} to {new_member.versus_trophies}",
        color=utils.Color.random().__str__(),
        timestamp=utils.get_time())
    embed.set_thumbnail(new_member.badge.url)
    await coc_plugin.app.rest.create_message(embed=embed,
                                             channel=channel
                                             )


@coc_client.event
@coc.ClientEvents.event_error()
async def on_event_error(exception):
    if isinstance(exception, coc.PrivateWarLog):
        return  # lets ignore private war log errors
    print("Uh oh! Something went wrong in coc.py events... printing traceback for you.")
    traceback.print_exc()


@coc_plugin.command()
@lightbulb.option("player_tag", "the Player tag of the Player", required=True, type=str)
@lightbulb.command("player_heroes", "all the Heros from a Player")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def player_heroes(ctx):
    player_tag = ctx.options.player_tag
    if not cocutils.is_valid_tag(player_tag):
        await ctx.send("You didn't give me a proper tag!")
        return

    try:
        player = await coc_client.get_player(player_tag)
    except coc.NotFound:
        await ctx.send("This player doesn't exist!")
        return

    to_send = ""
    for hero in player.heroes:
        to_send += "{}: Lv{}/{}\n".format(str(hero), hero.level, hero.max_level)
    if ctx.interaction:
        await ctx.respond(to_send, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(to_send, delete_after=40)


@coc_plugin.command()
@lightbulb.option("clan_tag", "The Clan-Tag of the Clan", required=True, type=str)
@lightbulb.command("clan_info", "Info about a given Clan")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def clan_info(ctx):
    clan_tag = ctx.options.clan_tag
    if not cocutils.is_valid_tag(clan_tag):
        await ctx.send("You didn't give me a proper tag!")
        return

    try:
        clan = await coc_client.get_clan(clan_tag)
    except coc.NotFound:
        if ctx.interaction:
            await ctx.respond("This Clan does not exist!", flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond("This Clan does not exist!", delete_after=20)
        return

    if clan.public_war_log is False:
        log = "Private"
    else:
        log = "Public"

    e = hikari.Embed(colour=discord.Colour.green().__str__())
    e.set_thumbnail(clan.badge.url)
    e.add_field(name="Clan Name", value=f"{clan.name}({clan.tag})\n[Open in game]({clan.share_link})", inline=False)
    e.add_field(name="Clan Level", value=clan.level, inline=False)
    e.add_field(name="Description", value=clan.description, inline=False)
    e.add_field(name="Leader", value=str(clan.get_member_by(role=coc.Role.leader)), inline=False)
    e.add_field(name="Clan Type", value=clan.type, inline=False)
    e.add_field(name="Location", value=clan.location, inline=False)
    e.add_field(name="Total Clan Trophies", value=str(clan.points), inline=False)
    e.add_field(name="Total Clan Versus Trophies", value=str(clan.versus_points), inline=False)
    e.add_field(name="WarLog Type", value=log, inline=False)
    e.add_field(name="Required Trophies", value=str(clan.required_trophies), inline=False)
    e.add_field(name="War Win Streak", value=str(clan.war_win_streak), inline=False)
    e.add_field(name="War Frequency", value=clan.war_frequency, inline=False)
    e.add_field(name="Clan War League Rank", value=clan.war_league, inline=False)
    e.add_field(name="Clan Labels", value="\n".join(label.name for label in clan.labels), inline=False)
    e.add_field(name="Member Count", value=f"{clan.member_count}/50", inline=False)
    e.add_field(
        name="Clan Record",
        value=f"Won - {clan.war_wins}\nLost - {clan.war_losses}\n Draw - {clan.war_ties}",
        inline=False
    )
    if ctx.interaction:
        await ctx.respond(embed=e, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=e, delete_after=40)


@coc_plugin.command()
@lightbulb.option("clan_tag", "The Clan-Tag of the Clan", required=True, type=str)
@lightbulb.command("clan_members", "Members of a given Clan")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def clan_member(ctx, clan_tag):
    if not cocutils.is_valid_tag(clan_tag):
        await ctx.send("You didn't give me a proper tag!")
        return

    try:
        clan = await coc_client.get_clan(clan_tag)
    except coc.NotFound:
        if ctx.interaction:
            await ctx.respond("This Clan does not exist!", flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond("This Clan does not exist!", delete_after=20)
        return

    member = ""
    for i, a in enumerate(clan.members, start=1):
        member += f"`{i}.` {a.name}\n"
    embed = hikari.Embed(colour=discord.Colour.red(), title=f"Members of {clan.name}", description=member)
    embed.set_thumbnail(clan.badge.url)
    embed.set_footer(text=f"Total Members - {clan.member_count}/50")
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=40)


@coc_plugin.command()
@lightbulb.option("clan_tag", "The Clan-Tag of the Clan", required=True, type=str)
@lightbulb.command("current_war_status", "Info about a War from a given Clan")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def current_war_status(ctx, clan_tag):
    if not cocutils.is_valid_tag(clan_tag):
        await ctx.send("You didn't give me a proper tag!")
        return

    e = discord.Embed(colour=discord.Colour.blue())

    try:
        war = await coc_client.get_current_war(clan_tag)
    except coc.PrivateWarLog:
        if ctx.interaction:
            await ctx.respond("Clan has a private war log!", flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond("Clan has a private war log!", delete_after=40)
        return

    if war is None:
        if ctx.interaction:
            await ctx.respond("Clan is in a strange CWL state!", flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond("Clan is in a strange CWL state!", delete_after=40)
        return

    e.add_field(name="War State:", value=war.state, inline=False)

    if war.end_time:  # if state is notInWar we will get errors

        hours, remainder = divmod(int(war.end_time.seconds_until), 3600)
        minutes, seconds = divmod(remainder, 60)

        e.add_field(name=war.clan.name, value=war.clan.tag)
        e.add_field(name="Opponent:", value=f"{war.opponent.name}\n" f"{war.opponent.tag}", inline=False)
        e.add_field(name="War End Time:", value=f"{hours} hours {minutes} minutes {seconds} seconds", inline=False)

    if ctx.interaction:
        await ctx.respond(embed=e, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=e, delete_after=40)


@coc_client.event
@coc.WarEvents.war_attack(tags=clan_tags)
async def current_war_stats(attack, war):
    channel = await coc_plugin.app.rest.fetch_channel(WAR_CHANNEL_ID)
    embed = hikari.Embed(
        title=f"Attack number {attack.order}\n({attack.attacker.map_position}).{attack.attacker} of {attack.attacker.clan} attacked ({attack.defender.map_position}).{attack.defender} of {attack.defender.clan}",
        color=utils.Color.random().__str__(),
        timestamp=utils.get_time())
    if isinstance(channel, hikari.GuildTextChannel):
        channel: hikari.GuildTextChannel = channel
        guild: hikari.guilds.PartialGuild = await channel.fetch_guild()
        url = guild.make_icon_url()
        if url:
            embed.set_thumbnail(url)
    await coc_plugin.app.rest.create_message(embed=embed,
                                             channel=channel
                                             )


@tasks.task(s=500)
async def coc_tasks():
    await asyncio.sleep(5)
    try:
        channel = await coc_plugin.app.rest.fetch_channel(INFORMATION_CHANNEL_ID)
        await utils.purge(channel.id, 5, coc_plugin.bot)
        clan_tag = clan_tags[0]
        try:
            war = await coc_client.get_current_war(clan_tag)
        except coc.PrivateWarLog:
            return
        if not cocutils.is_valid_tag(clan_tag):
            return
        try:
            clan = await coc_client.get_clan(clan_tag)
        except coc.NotFound:
            return
        channel: hikari.GuildTextChannel = channel
        guild: hikari.guilds.PartialGuild = await channel.fetch_guild()
        urllib.request.urlretrieve(clan.badge.url, "clan-badge.jpg")
        await guild.edit(icon="clan-badge.jpg")
        if clan.public_war_log is False:
            log = "Private"
        else:
            log = "Public"

        member = ""
        for i, a in enumerate(clan.members, start=1):
            member += f"[{i}.] {a.name} | {a.tag}\n"

        e = hikari.Embed(colour=discord.Colour.green().__str__())
        e.set_thumbnail(clan.badge.url)
        e.add_field(name="Clan Name", value=f"{clan.name}({clan.tag})\n[Open in game]({clan.share_link})", inline=False)
        e.add_field(name="Clan Level", value=clan.level, inline=False)
        e.add_field(name="Description", value=clan.description, inline=True)
        e.add_field(name="Leader", value=str(clan.get_member_by(role=coc.Role.leader)), inline=True)
        e.add_field(name="Clan Type", value=clan.type, inline=True)
        e.add_field(name="Location", value=clan.location, inline=True)
        e.add_field(name="Total Clan Trophies", value=str(clan.points), inline=True)
        e.add_field(name="Total Clan Versus Trophies", value=str(clan.versus_points), inline=True)
        e.add_field(name="WarLog Type", value=log, inline=True)
        e.add_field(name="Required Trophies", value=str(clan.required_trophies), inline=True)
        e.add_field(name="War Win Streak", value=str(clan.war_win_streak), inline=True)
        e.add_field(name="War Frequency", value=clan.war_frequency, inline=True)
        e.add_field(name="Clan War League Rank", value=clan.war_league, inline=True)
        e.add_field(name="Clan Labels", value="\n".join(label.name for label in clan.labels), inline=True)
        e.add_field(name="Member Count", value=f"{clan.member_count}/50", inline=True)
        e.add_field(
            name="Clan Record",
            value=f"Won - {clan.war_wins}\nLost - {clan.war_losses}\n Draw - {clan.war_ties}",
            inline=True
        )
        if war is None:
            pass
        else:
            e.add_field(name="War State:", value=war.state, inline=False)
            if war.end_time:  # if state is notInWar we will get errors

                hours, remainder = divmod(int(war.end_time.seconds_until), 3600)
                minutes, seconds = divmod(remainder, 60)
                e.add_field(name="Enemy:", value=f"{war.opponent.name}\n" f"{war.opponent.tag}", inline=True)
                e.add_field(name="War Ends In:", value=f"{hours} hours {minutes} min",
                            inline=True)
        e.add_field(name="Members", value=f"```ini\n{member}```", inline=False)
        await coc_plugin.app.rest.create_message(embed=e,
                                                 channel=channel
                                                 )
    except TypeError:
        pass


#coc_tasks.start()


def load(bot):
    bot.add_plugin(coc_plugin)


def unload(bot):
    bot.remove_plugin(coc_plugin)
