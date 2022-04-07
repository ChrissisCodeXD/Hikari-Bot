import hikari

from imports import *

wahlen_plugin = lightbulb.Plugin(name="server_managment.wahlen", description="Wahlen Plugin")


def savenewadmin(userid, aaa: dict) -> bool:
    """
    checkt ob ein user schon in den admins eingetragen ist und wenn nicht dann traegt er ihn ein und return True ansonsten return er False
    :param userid: int, str
    :return: bool
    """

    if isinstance(userid, int):
        userid = str(userid)

    if not userid in aaa["admins"]:
        aaa["admins"].append(userid)
        with open("./admins.json", "w") as e:
            json.dump(aaa, e, indent=4)
        return True
    return False


@wahlen_plugin.command()
@lightbulb.option("admin1", "the first admin you want to add", type=hikari.Member, required=True)
@lightbulb.option("admin2", "the second admin you want to add", type=hikari.Member, required=False)
@lightbulb.command("addadmin", description="adds an admin to the list of admins")
@lightbulb.implements(lightbulb.SlashCommand)
async def einreiche_command(ctx):
    """
    damit stellt man 2 admins auf.
    :param ctx:
    :param admin1:
    :param admin2:
    :return:
    """

    admin1 = ctx.options.admin1
    admin2 = ctx.options.admin2

    aaa = json.load(open("./admins.json", "r"))

    if str(ctx.author.id) in aaa["users"]:
        left = aaa["users"][str(ctx.author.id)]
    else:
        left = 2
    if admin2:
        if admin1.id == ctx.author.id or admin2.id == ctx.author.id: return await ctx.respond(
            "Du kannst dich nicht selber auftstellen!", flags=hikari.MessageFlag.EPHEMERAL)
        if left == 2:
            got_added = savenewadmin(admin1.id, aaa)
            if not got_added:
                await ctx.respond(f"{admin1} was already added to admins", flags=hikari.MessageFlag.EPHEMERAL)
            else:
                left -= 1
                await ctx.respond(f'added {admin1} to the admins', flags=hikari.MessageFlag.EPHEMERAL)
            got_added = savenewadmin(admin2.id, aaa)
            if not got_added:
                await ctx.respond(f"{admin2} was already added to admins", flags=hikari.MessageFlag.EPHEMERAL)
            else:
                left -= 1
                await ctx.respond(f'added {admin2} to the admins', flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(f"you can only add {left} more admins", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        if admin1.id == ctx.author.id: return await ctx.respond("Du kannst dich nicht selber auftstellen!",
                                                                flags=hikari.MessageFlag.EPHEMERAL)
        if left > 0:
            got_added = savenewadmin(admin1.id, aaa)
            if not got_added:
                await ctx.respond(f"{admin1} was already added to admins", flags=hikari.MessageFlag.EPHEMERAL)
            else:
                left -= 1
                await ctx.respond(f'added {admin1} to the admins', flags=hikari.MessageFlag.EPHEMERAL)

        else:
            await ctx.respond(f"you can only add {left} more admins", flags=hikari.MessageFlag.EPHEMERAL)
    aaa["users"][str(ctx.author.id)] = left
    with open("./admins.json", "w") as e:
        json.dump(aaa, e, indent=4)


@wahlen_plugin.command()
@lightbulb.command("clearvotes", description="clears all votes")
@lightbulb.implements(lightbulb.SlashCommand)
async def clearvots_command(ctx):
    deleteallchooses(ctx.author.id)
    await ctx.respond(f"Every Vote from u is now deleted!", flags=hikari.MessageFlag.EPHEMERAL)


@wahlen_plugin.command()
@lightbulb.command("seevotes", description="shows all votes")
@lightbulb.implements(lightbulb.SlashCommand)
async def seevotes_command(ctx):
    tosend = {}
    print("a")
    if not ctx.author.id == 636998030666629120 and not ctx.author.id == 589898942527963157: return
    guild: hikari.Guild = ctx.get_guild()
    aaa = json.load(open("./admins.json", "r"))
    for i in aaa["abstimmung"]:
        tosend[f"{guild.get_member(i)}"] = []
    for i in aaa["abstimmung"]:
        for k in aaa["abstimmung"][str(i)]:
            tosend[f"{guild.get_member(i)}"].append(f"{guild.get_member(k)}")
    message = ""
    for i in tosend:
        message += f"**{i}**\n"
        for k in tosend[i]:
            message += f"   {k}\n"
    await ctx.author.send(message)


async def gen_rows(bot, aaa, guild):
    rows: t.list[lightbulb.ActionRow] = []
    row = bot.rest.build_action_row()
    select = row.add_select_menu("wahlen")
    select.set_placeholder("Waehle maximal 2 Admins")
    for k, i in enumerate(aaa["admins"]):

        label = str(guild.get_member(i))
        if label:
            select.add_option(label, str(i)).add_to_menu()

    select.add_to_container()
    rows.append(row)

    return rows


@wahlen_plugin.command()
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command("sendwahll", description="votes for a user")
@lightbulb.implements(lightbulb.SlashCommand)
async def sendwahll_command(ctx):
    """
    sendet die nachricht zum abstimmen
    :param ctx:
    :return:
    """

    aaa = json.load(open("./admins.json", "r"))
    guild: hikari.Guild = ctx.get_guild()
    admins = ""

    for k, i in enumerate(aaa["admins"]):
        user = guild.get_member(i)

        admins += f'`{k + 1}.` {user.mention}\n'
        aaa["abstimmung"][str(i)] = []

    rows = await gen_rows(ctx.bot, aaa, guild)

    with open("./admins.json", "w") as e:
        json.dump(aaa, e, indent=4)

    embed = hikari.Embed(title=f"Adminwahl",
                         description=f'Es stehen nun wieder neue adminwahlen an. Die folgenden Personen wurden aufgestellt: \n{admins}')
    msg = await ctx.respond(embed=embed, components=rows)
    msg = await msg.message()
    aaa["channel"] = msg.channel_id
    aaa["message"] = msg.id
    with open("./admins.json", "w") as e:
        json.dump(aaa, e, indent=4)


def hasselected(user: int):
    """
    checkt ob der User schon geweahlt hat und wie oft
    :param user:
    :return:
    """
    aaa = json.load(open("./admins.json", "r"))
    toreturn = 0
    for i in aaa["abstimmung"]:
        for i2 in aaa["abstimmung"][i]:
            if i2 == str(user):
                toreturn += 1

    return toreturn


async def updatemessage(bot, guild):
    """
    updated die nachricht zum waehlen damit man immer sieht wieviele stimmen es gerade sind
    :param ctx:
    :return:
    """
    aaa = json.load(open("./admins.json", "r"))
    admins = ""

    for k, i in enumerate(aaa["admins"]):
        user = guild.get_member(i)

        admins += f'`{k + 1}.` {user.mention}\n'
        aaa["abstimmung"][str(i)] = []

    rows = await gen_rows(bot, aaa, guild)

    with open("./admins.json", "w") as e:
        json.dump(aaa, e, indent=4)
    embed = hikari.Embed(title=f"Adminwahl",
                         description=f'Es stehen nun wieder neue adminwahlen an. Die folgenden Personen wurden aufgestellt: \n{admins}')

    await utils.purge(aaa["channel"], 20, bot)
    channel = guild.get_channel(aaa["channel"])
    msg = await channel.send(embed=embed, components=rows)
    aaa["message"] = msg.id
    with open("./admins.json", "w") as e:
        json.dump(aaa, e, indent=4)


def deleteallchooses(user: int):
    user = str(user)
    aaa = json.load(open("./admins.json", "r"))
    for i in aaa["abstimmung"]:

        for i2 in aaa["abstimmung"][i]:
            if i2 == user:
                aaa["abstimmung"][i].remove(i2)

    with open("./admins.json", "w") as e:
        json.dump(aaa, e, indent=4)


@wahlen_plugin.listener(hikari.InteractionCreateEvent)
async def wahlen(event: hikari.InteractionCreateEvent):
    """
    wird getriggert wenn jemand eine person waehlt
    :param ctx:
    :return:
    """

    e = event
    if not isinstance(e.interaction, hikari.ComponentInteraction): return
    i: hikari.ComponentInteraction = e.interaction
    guild = i.get_guild()
    if not i.guild_id: return
    if not i.custom_id == "wahlen": return

    hashchoosen = False
    await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE,
                                    "Wahl wird verarbeitet... Bitte warte ein bisschen (Das ganze dauert ein bisschen laenger aufgrund der Datensicherheit des Codes)",
                                    flags=hikari.MessageFlag.EPHEMERAL)
    aaa = json.load(open("./admins.json", "r"))
    selected = hasselected(user=i.member.id)
    # await ctx.defer(ignore=True)
    print(i.values)
    if selected >= 2:
        await i.edit_initial_response("You already choose 2 People!")

    elif str(i.member.id) in aaa["abstimmung"][i.values[0]]:
        await i.edit_initial_response("You cannot choose the same Person 2 Times!")
    else:
        print("aaaa")
        aaa["abstimmung"][i.values[0]].append(str(i.member.id))
        print(aaa)

        hashchoosen = True

    if hashchoosen == True:
        await i.edit_initial_response("Wahl verarbeitet!")

    await updatemessage(e.interaction.app, guild)

    with open("./admins.json", "w") as ee:
        json.dump(aaa, ee, indent=4)


def load(bot):
    bot.add_plugin(wahlen_plugin)


def unload(bot):
    bot.remove_plugin(wahlen_plugin)
