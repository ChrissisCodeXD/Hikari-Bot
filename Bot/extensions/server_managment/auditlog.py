import hikari
import lightbulb

import utils
from imports import *
from Bot.DataBase.aduitlogsys import DBAuditLog
from Bot.DataBase.logChannel import DBlog

auditlog_plugin = lightbulb.Plugin("server_managment.plugin")

auditlog_plugin.add_checks(
    lightbulb.checks.guild_only,
)

buttons = ["ban",
           "guild_change",
           "channel_change",
           "invites",
           "member",
           "message",
           "role",
           "voice"]

labels = {
    "ban": "Ban",
    "guild_change": "Guild",
    "channel_change": "Channel",
    "invites": "Invites",
    "member": "Member",
    "message": "Message",
    "role": "Role",
    "voice": "Voice Talk",
}


async def build_rows(bot, guild_id):
    guild_id = int(guild_id)
    rows = []

    row = bot.rest.build_action_row()
    settings = DBAuditLog(bot.db).get_settings(guild_id)

    for i, k in enumerate(settings):
        label = labels[k]
        if i % 4 == 0 and i != 0:
            rows.append(row)
            row = bot.rest.build_action_row()

        (
            row.add_button(
                hikari.ButtonStyle.SUCCESS if settings[k] else hikari.ButtonStyle.DANGER,
                k
            )
                .set_label(label)
                .set_emoji("✔" if settings[k] else "✖")
                .add_to_container()
        )

    rows.append(row)

    return rows


@auditlog_plugin.command()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("auditlog", "The Auditlog System")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def auditlog(ctx: lightbulb.Context):
    pass


@auditlog.child()
@lightbulb.command("settings", "The Auditlog Settings", inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def settings(ctx: lightbulb.Context):
    rows = await build_rows(ctx.app, ctx.guild_id)
    settings = DBAuditLog(ctx.app.db).get_settings(ctx.guild_id)
    embed = hikari.Embed(
        title="Auditlog Settings",
        description="Change the Auditlog Settings",
        color=utils.Colour.green().__str__(),
        timestamp=utils.get_time()
    )
    for i in settings:
        embed.add_field(
            name=labels[i],
            value="``` " + ("✅ - on" if settings[i] else "❌ - off") + " ```",
            inline=True)
    res = DBlog(ctx.app.db).get_dict(ctx.guild_id)

    embed.add_field(
        name="Auditlog Channel",
        value=f"``` {ctx.get_guild().get_channel(res['audit_log']).name if res['audit_log'] != 0 else '❌ - Not Set'}```",
    )

    embed.add_field(
        "How to set the Channel?",
        "You can set the Channel to send the Auditlog in by using `/auditlog addchannel <channel>`",
    )
    await ctx.respond(embed=embed, components=rows)


@auditlog_plugin.listener(hikari.events.InteractionCreateEvent)
async def on_interaction(event: hikari.events.InteractionCreateEvent):
    e = event
    if isinstance(e.interaction, hikari.ComponentInteraction):
        i: hikari.ComponentInteraction = e.interaction
        if i.custom_id in buttons:
            res = await utils.mod_check_without_ctx(bot=i.app, guild_id=i.guild_id, member=i.member)
            if res or i.member.permissions & hikari.Permissions.MANAGE_GUILD:
                settings = DBAuditLog(i.app.db).get_settings(i.guild_id)
                onoroff = settings[i.custom_id]
                new_value = "abcdefghijklmnopqrstuvwxyz"
                match onoroff:
                    case False:
                        new_value = 1
                    case True:
                        new_value = 0
                if new_value == "abcdefghijklmnopqrstuvwxyz": return
                DBAuditLog(i.app.db).set(i.guild_id, i.custom_id, new_value)
                settings = DBAuditLog(i.app.db).get_settings(i.guild_id)
                embed = hikari.Embed(title="Auditlog Settings Updated",
                                     description="Settings for the Auditlog System have been updated",
                                     color=utils.Color.green().__str__(),
                                     timestamp=utils.get_time())
                embed.add_field(f"Updated: {i.custom_id}",
                                f"``` {'❌ - off' if new_value == 0 else '✅ - on'}```",
                                inline=True)
                await i.create_initial_response(response_type=hikari.ResponseType.MESSAGE_CREATE, embed=embed,
                                                flags=hikari.MessageFlag.EPHEMERAL)

                embed = hikari.Embed(
                    title="Auditlog Settings",
                    description="Change the Auditlog Settings",
                    color=utils.Colour.green().__str__(),
                    timestamp=utils.get_time()
                )
                for h in settings:
                    embed.add_field(
                        name=labels[h],
                        value="``` " + ("✅ - on" if settings[h] else "❌ - off") + " ```",
                        inline=True)

                res = DBlog(i.app.db).get_dict(i.guild_id)

                embed.add_field(
                    name="Auditlog Channel",
                    value=f"``` {event.interaction.get_guild().get_channel(res['audit_log']).name if res['audit_log'] != 0 else '❌ - Not Set'}```",
                )

                embed.add_field(
                    "How to set the Channel?",
                    "You can set the Channel to send the Auditlog in by using `/auditlog addchannel <channel>`",
                )
                rows = await build_rows(i.app, i.guild_id)
                await i.message.edit(embed=embed, components=rows)
            else:
                embed = hikari.Embed(title="❌ Error",
                                     description="You are not allowed to use this",
                                     color=utils.Color.red().__str__(), timestamp=utils.get_time())
                await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, embed=embed,
                                                flags=hikari.MessageFlag.EPHEMERAL)


@auditlog.child()
@lightbulb.option("channel", "The Channel to send audit log in", type=hikari.TextableGuildChannel)
@lightbulb.command("add", "Add the Channel to send the audit log in", inherit_checks=True)
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def add(ctx: lightbulb.Context):
    channel = ctx.options.channel
    type = "audit_log"

    res = DBlog(ctx.app.db).add_log_channel(ctx.guild_id, type, channel.id)

    if not res:
        embed = hikari.Embed(
            title="❌ Error",
            description="The channel is already a Audit Log channel",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )

        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
    else:
        channel = ctx.get_guild().get_channel(channel.id)
        embed = hikari.Embed(
            title="✅ Success",
            description=f"The channel {channel.mention} is now the Audit-log channel",
            color=utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)


@auditlog.child()
@lightbulb.command("remove", "Remove the Channel to send the audit log in", inherit_checks=True)
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def remove(ctx: lightbulb.Context):
    type = "audit_log"
    res = DBlog(ctx.app.db).remove_audit_log_channel(ctx.guild_id)

    embed = hikari.Embed(
        title="✅ Success",
        description="Audit-log channel removed",
        color=utils.Color.green().__str__(),
        timestamp=utils.get_time()
    )

    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=5)


def load(bot):
    bot.add_plugin(auditlog_plugin)


def unload(bot):
    bot.remove_plugin(auditlog_plugin)
