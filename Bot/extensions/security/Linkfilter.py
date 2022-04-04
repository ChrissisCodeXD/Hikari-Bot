import hikari.guilds
import lightbulb

from imports import *
from Bot.DataBase.LinkSystem import DBLink
from hikari.api import ActionRowBuilder

buttons = {
    "social_media": "social_button",
    "google": "google_button",
    "bitly": "bitly_button",
    "all_links": "all_links_button",
    "discord": "discord_button",
    "gif": "gif_button"
}


async def create_actionrows(bot: lightbulb.BotApp, guild_id) -> t.Iterable[ActionRowBuilder]:
    settings = DBLink(bot.db).get_settings(guild_id)
    if not settings:
        settings = DBLink(bot.db).create_settings(guild_id)

    """generatres the actionrows for the linkfilter settings"""
    rows: t.list[lightbulb.ActionRow] = []

    row = bot.rest.build_action_row()

    for i, button in enumerate(buttons):
        if i % 5 == 0 and i != 0:
            rows.append(row)
            row = bot.rest.build_action_row()

        label = button.replace("_", " ").title()

        (
            row.add_button(
                hikari.ButtonStyle.SUCCESS if settings[button] else hikari.ButtonStyle.DANGER,
                button,
            )
                .set_label(label)
                .set_emoji("✔" if settings[button] else "✖")
                .add_to_container()

        )
    rows.append(row)

    return rows


link_plugin = lightbulb.Plugin("Linkfilter", "Filters out links from messages")

link_plugin.add_checks(
    lightbulb.checks.guild_only,

)


@link_plugin.command()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("linkfilter", "the linkfilter System")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def link(ctx: lightbulb.Context):
    pass


@link.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("settings", "the linkfilter Systems Settings")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def settings(ctx: lightbulb.Context):
    settings = DBLink(ctx.app.db).get_settings(ctx.guild_id)
    if not settings:
        settings = DBLink(ctx.app.db).create_settings(ctx.guild_id)
    embed = hikari.Embed(title="Linkfilter Settings",
                         description="Settings for the linkfilter System",
                         color=utils.Color.green().__str__(),
                         timestamp=utils.get_time())
    embed.add_field("Social Media",
                    f"``` {'❌ - off' if not settings['social_media'] else '✅ - on'}```",
                    inline=True)
    embed.add_field("Google",
                    f"``` {'❌ - off' if not settings['google'] else '✅ - on'}```",
                    inline=True)
    embed.add_field("Bitly",
                    f"``` {'❌ - off' if not settings['bitly'] else '✅ - on'}```",
                    inline=True)
    embed.add_field("Discord",
                    f"``` {'❌ - off' if not settings['discord'] else '✅ - on'}```",
                    inline=True)
    embed.add_field("GIF",
                    f"``` {'❌ - off' if not settings['gif'] else '✅ - on'}```",
                    inline=True)
    embed.add_field("All Links",
                    f"``` {'❌ - off' if not settings['all_links'] else '✅ - on'}```",
                    inline=True)
    ignored_roles = []
    for role in settings["ignored_roles"]:
        role: hikari.guilds.PartialRole = ctx.get_guild().get_role(role)
        ignored_roles.append(role.name)

    ignored_roles = ',\n'.join(ignored_roles) if settings['ignored_roles'] else "❌ - empty"
    embed.add_field("Ignored Roles", f"```{ignored_roles}```", inline=True)

    ignored_users = []
    for role in settings["ignored_users"]:
        user: hikari.guilds.Member = ctx.get_guild().get_member(role)
        ignored_users.append(user.username)

    ignored_users = ',\n'.join(ignored_users) if settings['ignored_users'] else "❌ - empty"
    embed.add_field("Ignored Users", f"```{ignored_users}```", inline=True)

    embed.add_field("How to use",
                    "Use the buttons to toggle the settings. \n"
                    "If the Buttons is red it is off, if it is green it is on.\n"
                    "You can also use the command \n `linkfilter toggle <social_media/google/bitly/all_links>`\nto toggle the settings.",
                    inline=False)

    rows = await create_actionrows(ctx.bot, ctx.guild_id)
    await ctx.respond(embed=embed, components=rows)


@link_plugin.listener(hikari.events.InteractionCreateEvent)
async def on_interaction(event: hikari.events.InteractionCreateEvent):
    e = event
    if isinstance(e.interaction, hikari.ComponentInteraction):
        i: hikari.ComponentInteraction = e.interaction
        if i.custom_id in buttons:
            res = await utils.mod_check_without_ctx(bot=i.app, guild_id=i.guild_id, member=i.member)
            if res or i.member.permissions & hikari.Permissions.ADMINISTRATOR:
                settings = DBLink(i.app.db).get_settings(i.guild_id)
                if not settings:
                    settings = DBLink(i.app.db).create_settings(i.guild_id)
                onoroff = settings[i.custom_id]
                new_value = "abcdefghijklmnopqrstuvwxyz"
                match onoroff:
                    case 0:
                        new_value = 1
                    case 1:
                        new_value = 0
                if new_value == "abcdefghijklmnopqrstuvwxyz": return
                DBLink(i.app.db).update_settings(i.guild_id, i.custom_id, new_value)
                settings = DBLink(i.app.db).get_settings(i.guild_id)
                embed = hikari.Embed(title="Linkfilter Updated",
                                     description="Settings for the linkfilter System have been updated",
                                     color=utils.Color.green().__str__(),
                                     timestamp=utils.get_time())
                embed.add_field(f"Updated: {i.custom_id}",
                                f"``` {'❌ - off' if new_value == 0 else '✅ - on'}```",
                                inline=True)
                await i.create_initial_response(response_type=hikari.ResponseType.MESSAGE_CREATE, embed=embed,
                                                flags=hikari.MessageFlag.EPHEMERAL)

                embed = hikari.Embed(title="Linkfilter Settings",
                                     description="Settings for the linkfilter System",
                                     color=utils.Color.green().__str__(),
                                     timestamp=utils.get_time())
                embed.add_field("Social Media",
                                f"``` {'❌ - off' if not settings['social_media'] else '✅ - on'}```",
                                inline=True)
                embed.add_field("Google",
                                f"``` {'❌ - off' if not settings['google'] else '✅ - on'}```",
                                inline=True)
                embed.add_field("Bitly",
                                f"``` {'❌ - off' if not settings['bitly'] else '✅ - on'}```",
                                inline=True)
                embed.add_field("Discord",
                                f"``` {'❌ - off' if not settings['discord'] else '✅ - on'}```",
                                inline=True)
                embed.add_field("GIF",
                                f"``` {'❌ - off' if not settings['gif'] else '✅ - on'}```",
                                inline=True)
                embed.add_field("All Links",
                                f"``` {'❌ - off' if not settings['all_links'] else '✅ - on'}```",
                                inline=True)
                ignored_roles = []
                for role in settings["ignored_roles"]:
                    role: hikari.guilds.PartialRole = i.get_guild().get_role(role)
                    ignored_roles.append(role.name)

                ignored_roles = ',\n'.join(ignored_roles) if settings['ignored_roles'] else "❌ - empty"
                embed.add_field("Ignored Roles", f"```{ignored_roles}```", inline=True)

                ignored_users = []
                for role in settings["ignored_users"]:
                    user: hikari.guilds.Member = i.get_guild().get_member(role)
                    ignored_users.append(user.username)

                ignored_users = ',\n'.join(ignored_users) if settings['ignored_users'] else "❌ - empty"
                embed.add_field("Ignored Users", f"```{ignored_users}```", inline=True)

                embed.add_field("How to use",
                                "Use the buttons to toggle the settings. \n"
                                "If the Buttons is red it is off, if it is green it is on.\n"
                                "You can also use the command \n `/linkfilter toggle <social_media/google/bitly/all_links>`\nto toggle the settings.",
                                inline=False)
                rows = await create_actionrows(i.app, i.guild_id)
                await i.message.edit(embed=embed, components=rows)
            else:
                embed = hikari.Embed(title="❌ Error",
                                     description="You are not allowed to use this",
                                     color=utils.Color.red().__str__(), timestamp=utils.get_time())
                await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, embed=embed,
                                                flags=hikari.MessageFlag.EPHEMERAL)


@link.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("blocker", "What you want to block",
                  choices=["social_media", "google", "bitly", "discord", "GIF", "all_links"], required=True)
@lightbulb.command(name="toggle", description="Toggle the settings for the linkfilter System")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def toggle(ctx: lightbulb.Context):
    """
    Toggle the settings for the linkfilter System
    """
    settings = DBLink(ctx.app.db).get_settings(ctx.guild_id)
    if not settings:
        settings = DBLink(ctx.app.db).create_settings(ctx.guild_id)
    onoroff = settings[ctx.options.blocker]
    new_value = "abcdefghijklmnopqrstuvwxyz"
    match onoroff:
        case 0:
            new_value = 1
        case 1:
            new_value = 0
    if new_value == "abcdefghijklmnopqrstuvwxyz": return
    DBLink(ctx.app.db).update_settings(ctx.guild_id, ctx.options.blocker, new_value)
    settings = DBLink(ctx.app.db).get_settings(ctx.guild_id)
    embed = hikari.Embed(title="Linkfilter Updated",
                         description="Settings for the linkfilter System have been updated",
                         color=utils.Color.green().__str__(),
                         timestamp=utils.get_time())
    embed.add_field(f"Updated: {ctx.options.blocker}",
                    f"``` {'❌ - off' if new_value == 0 else '✅ - on'}```",
                    inline=True)
    embed.add_field("To see the settings use:", "`/linkfilter settings`", inline=False)
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=10)


@link_plugin.listener(hikari.events.GuildMessageCreateEvent)
async def on_message(event: hikari.events.GuildMessageCreateEvent):
    if not event.message.content: return
    e = event
    settings = DBLink(event.app.db).get_settings(event.guild_id)
    if not settings:
        settings = DBLink(event.app.db).create_settings(event.guild_id)
    if e.author_id in settings["ignored_users"]: return
    for i in e.member.role_ids:
        if i in settings["ignored_roles"]: return

    if not e.message.content: return

    event = utils.OnLinkProtectMessageCreate(
        app=e.app,
        original_event=e,
        message=e.message,
        settings=settings
    )

    await link_plugin.bot.dispatch(event)


@link_plugin.listener(utils.OnLinkProtectMessageCreate)
async def on_link_message(event: utils.OnLinkProtectMessageCreate):
    e: utils.OnLinkProtectMessageCreate = event
    oe: hikari.GuildMessageCreateEvent = e.original_event
    msg: hikari.Message = e.message
    stg: dict = e.settings

    active_filters = [i for i, e in stg.items() if e]

    if not active_filters: return

    link_filter = utils.LinkFilter(app=e.app,
                                   msg=msg)

    if "social_media" in active_filters:
        await link_filter.is_social_media()

    if "google" in active_filters:
        await link_filter.is_google()

    if "bitly" in active_filters:
        await link_filter.is_bitly()

    if "discord" in active_filters:
        await link_filter.is_discord()

    if "GIF" in active_filters:
        await link_filter.is_gif()

    if "all_links" in active_filters:
        await link_filter.is_link()

    return


def load(bot):
    bot.add_plugin(link_plugin)


def unload(bot):
    bot.remove_plugin(link_plugin)
