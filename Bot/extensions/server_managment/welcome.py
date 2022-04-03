import hikari
import lightbulb
from imports import *
from Bot.DataBase.welcome import *

welcome_plugin = lightbulb.Plugin("server-managment.welcome")

welcome_plugin.add_checks(
    lightbulb.checks.guild_only,
    lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR),
)


# async def _check(member: hikari.guilds.Member):
#    if not DBWelcome(welcome_plugin.app.db).indata(member.guild_id):
#        # TODO
#        pass


@welcome_plugin.command()
@lightbulb.command("welcome", "welcome system")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def welcome(ctx: lightbulb.Context) -> None:
    pass


utils.Color
banner_options = ["anime", "black", "fortnite"]
banner_colors = ["teal", "dark_teal", "green", "dark_green", "blue", "dark_blue", "purple", "magenta", "dark_magenta",
                 "gold", "dark_gold", "orange", "dark_orange", "red", "dark_red", "lighter_grey", "dark_grey",
                 "light_grey"
                 "darker_grey", "blurple", "greyple", "dark_theme"]


@welcome.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("list", "list all welcome channels")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def welcome_list(ctx: lightbulb.Context) -> None:
    channels = DBWelcomeChannel(welcome_plugin.app.db).get_channels(ctx.get_guild().id)
    if not channels:
        embed = hikari.Embed(title="❌ Error",
                             description="There are no welcome channels",
                             color=utils.Color.red().__str__(), timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
        return
    embed = hikari.Embed(title="Welcome Channels",
                         description="\n".join([f"<#{channel[0]}>" for channel in channels]),
                         color=utils.Color.green().__str__(), timestamp=utils.get_time())
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=5)
    return


@welcome.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("channel", "The Channel to send Welcome Message", type=hikari.TextableGuildChannel, required=False)
@lightbulb.option("message", "The Message to send", type=str, required=False)
@lightbulb.option("banner", "If you want to use a banner", type=bool, required=False)
@lightbulb.option("banner_background", "The banner background", type=str, required=False, choices=banner_options)
@lightbulb.option("color", "The color of the Embed", type=str, required=False, choices=banner_colors)
@lightbulb.command("add", "add a welcome Channel")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def welcome_add(ctx: lightbulb.Context) -> None:
    banner_background = ctx.options.banner_background if ctx.options.banner_background else "black"
    banner_color = ctx.options.color if ctx.options.color else "default"

    match banner_background:
        case "anime":
            banner_background = "https://i.imgur.com/iPzjoqN.jpg"
        case "black":
            banner_background = "https://cdn.discordapp.com/attachments/765605082674364436/959526798104875068/Neues_Projekt_1.png"
        case "fortnite":
            banner_background = "https://cdn.discordapp.com/attachments/765605082674364436/959528360298565803/unnamed.png"
    match banner_color:
        case "default":
            banner_color = utils.Color.default().__str__()
        case "teal":
            banner_color = utils.Color.teal().__str__()
        case "dark_teal":
            banner_color = utils.Color.dark_teal().__str__()
        case "green":
            banner_color = utils.Color.green().__str__()
        case "dark_green":
            banner_color = utils.Color.dark_green().__str__()
        case "blue":
            banner_color = utils.Color.blue().__str__()
        case "dark_blue":
            banner_color = utils.Color.dark_blue().__str__()
        case "purple":
            banner_color = utils.Color.purple().__str__()
        case "magenta":
            banner_color = utils.Color.magenta().__str__()
        case "dark_magenta":
            banner_color = utils.Color.dark_magenta().__str__()
        case "gold":
            banner_color = utils.Color.gold().__str__()
        case "dark_gold":
            banner_color = utils.Color.dark_gold().__str__()
        case "orange":
            banner_color = utils.Color.orange().__str__()
        case "dark_orange":
            banner_color = utils.Color.dark_orange().__str__()
        case "red":
            banner_color = utils.Color.red().__str__()
        case "dark_red":
            banner_color = utils.Color.dark_red().__str__()
        case "lighter_grey":
            banner_color = utils.Color.lighter_grey().__str__()
        case "dark_grey":
            banner_color = utils.Color.dark_grey().__str__()
        case "light_grey":
            banner_color = utils.Color.light_grey().__str__()
        case "darker_grey":
            banner_color = utils.Color.darker_grey().__str__()
        case "blurple":
            banner_color = utils.Color.blurple().__str__()
        case "greyple":
            banner_color = utils.Color.greyple().__str__()
        case "dark_theme":
            banner_color = utils.Color.dark_theme().__str__()

    channel = ctx.options.channel if ctx.options.channel else ctx.get_channel()
    message = ctx.options.message

    if len(message) == 0 or message.strip() == "":
        if ctx.interaction:
            await ctx.respond("Please provide a message", flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond("Please provide a message", delete_after=5)
        return

    banner = 1 if ctx.options.banner else 0
    guild = ctx.get_guild()
    if not message:
        message = "Welcome to `{guild} `, **{member}**!\nPlease read the rules and have fun!\n"
    if not channel or not channel.type == hikari.ChannelType.GUILD_TEXT:
        embed = hikari.Embed(title="❌ Error",
                             description="Please provide a valid channel\n You can only use TextChannels for Welcome Channels",
                             color=utils.Color.red().__str__(), timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
        return
    channell = DBWelcomeChannel(welcome_plugin.app.db).is_channel_indb(ctx.get_guild().id, channel.id)
    if channell:
        embed = hikari.Embed(title="❌ Error",
                             description="This channel is already a Welcome Channel",
                             color=utils.Color.red().__str__(), timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
        return
    DBWelcomeChannel(welcome_plugin.app.db).add_channel(guild.id, channel.id, message, banner, banner_background,
                                                        banner_color)
    embed = hikari.Embed(title="✅ Success",
                         description="Welcome Channel added",
                         color=utils.Color.green().__str__(), timestamp=utils.get_time())
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=5)
    return


@welcome.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("help", "help for the welcome system")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def welcome_help(ctx):
    embed = hikari.Embed(title="Welcome System Help",
                         description="This is the help for the Welcome System",
                         color=utils.Color.green().__str__(), timestamp=utils.get_time())
    embed.add_field(name="Welcome System",
                    value="This is the welcome system, it will send a message to a channel when a new member joins the server.\n"
                          "You can use the following variables in the message:\n"
                          "`{member}` - The new member\n"
                          "`{guild}` - The guild name\n"
                          "`{guild_id}` - The guild id\n"
                          "`{member_count}` - The guild member count\n"
                          "`{member_id}` - The member id"
                    )
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=5)
    return


@welcome.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("channel", "The Channel to remove", type=hikari.TextableGuildChannel, required=True)
@lightbulb.command("remove", "remove a welcome Channel")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def welcome_remove(ctx: lightbulb.Context) -> None:
    channel = ctx.options.channel
    if not channel or not channel.type == hikari.ChannelType.GUILD_TEXT:
        embed = hikari.Embed(title="❌ Error",
                             description="Please provide a valid channel\n You can only use TextChannels for Welcome Channels",
                             color=utils.Color.red().__str__(), timestamp=utils.get_time())
        await ctx.respond(embed=embed)
        return
    channell = DBWelcomeChannel(welcome_plugin.app.db).is_channel_indb(ctx.get_guild().id, channel.id)
    if not channell:
        embed = hikari.Embed(title="❌ Error",
                             description="This channel is not a Welcome Channel",
                             color=utils.Color.red().__str__(), timestamp=utils.get_time())
        await ctx.respond(embed=embed)
        return
    DBWelcomeChannel(welcome_plugin.app.db).remove_channel(ctx.get_guild().id, channel.id)
    embed = hikari.Embed(title="✅ Success",
                         description="Welcome Channel removed",
                         color=utils.Color.green().__str__(), timestamp=utils.get_time())
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=5)
    return


@welcome_plugin.listener(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    check = DBWelcomeChannel(welcome_plugin.app.db).indata(event.get_guild().id)
    guild = event.get_guild()
    if check:
        for i in check:
            channel = event.get_guild().get_channel(i[2])
            if channel:
                embed = hikari.Embed(
                    title=i[3].format(
                        member=event.member,
                        guild=event.get_guild(),
                        guild_id=event.get_guild().id,
                        member_count=event.get_guild().member_count,
                        member_id=event.member.id
                    ),
                    timestamp=utils.get_time(),
                    color=i[6]
                )
                if i[4] == 1:
                    banner = await utils.get_banner(event.member, event.get_guild(), i[5])
                    embed.set_image(open(banner, "rb").read())
                    await channel.send(embed=embed)
    return

    return

    """     
    if event.guild_id == 952871675375022141:
        guild = event.get_guild()
        channel = await welcome_plugin.app.rest.fetch_channel(952871675916058638)
        embed = hikari.Embed(title=f'Welcome ** {event.member} ** to the KT-Clan Server! ',
                             description=f'Great to see you, ** {event.member} **! 😀 ',
                             color=0x0091ff)
        embed.set_image(
            guild.make_icon_url())
        await channel.send(embed=embed)
    pass
    """


def load(bot):
    bot.add_plugin(welcome_plugin)


def unload(bot):
    bot.remove_plugin(welcome_plugin)
