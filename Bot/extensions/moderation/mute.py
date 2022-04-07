import hikari
import lightbulb

import utils
from imports import *
from Bot.DataBase.mutesys import DBMute
from lightbulb.ext import tasks

mute_plugin = lightbulb.Plugin("moderation.mute_plugin")
mute_plugin.add_checks(
    lightbulb.checks.guild_only,
    lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)


async def on_mute_remove(ctx: lightbulb.Context, user: hikari.Member = None, cid=None):
    if not user and not cid: return
    if not user:
        res = DBMute(ctx.app.db).get_mute(cid)
        user = ctx.get_guild().get_member(res[0][3])
        if not user: return
    settings = DBMute(ctx.app.db).get_settings(ctx.guild_id)
    mutes = DBMute(ctx.app.db).get_all_for_user(user.id, ctx.guild_id)
    if not mutes:
        guild = ctx.get_guild()
        role = guild.get_role(settings[str(ctx.guild_id)])
        if role.id in user.role_ids:
            await user.remove_role(role, reason=f"Unmuting")


async def _check(ctx: lightbulb.Context):
    result = DBMute(ctx.app.db).get_settings(ctx.guild_id)
    role = None
    toret = None
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
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed)
        role = await ctx.app.rest.create_role(
            guild=ctx.get_guild(),
            name="Muted",
            mentionable=False,
            reason=f"Setting up the Mute System"
        )
        guild = await ctx.get_guild().fetch_self()

        for i in guild.get_channels():
            if not type(i) == hikari.GuildChannel: i = guild.get_channel(i)
            await i.edit_overwrite(
                target=role,
                deny=mute_perms,
                reason=f"Setting up the Mute System"
            )
        DBMute(ctx.app.db).add_settings(guild.id, role.id)
        embed = hikari.Embed(
            title="Finished setting up the Mute system.",
            color=utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.edit_last_response(embed=embed, delete_after=5)
    else:
        toret = True
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
                target_type=i.type,
                target=role,
                deny=mute_perms,
                reason=f"Setting up the Mute System"
            )
    return toret


@mute_plugin.command()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("mute", "Mute System")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def mute(ctx: lightbulb.Context) -> None:
    ret = await _check(ctx)
    if ret:
        embed = hikari.Embed(
            title=f"❌ Mute System is already setup!",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=10)


@mute.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("id", "The Mute-ID from the Mute you want to delete!", required=False)
@lightbulb.option("member", "The Member you want to delete the Mutes from", hikari.Member, required=False)
@lightbulb.command("delete", "Deletes The Mutes from a given Member or from Mute-ID", inherit_checks=True)
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def mute_delete(ctx: lightbulb.Context):
    async with ctx.get_channel().trigger_typing():
        await _check(ctx)
        if not ctx.interaction: await ctx.event.message.delete()
        if 'delete' in ctx.raw_options: del ctx.raw_options['delete']
        settings = DBMute(ctx.app.db).get_settings(ctx.get_guild().id)
        role = ctx.get_guild().get_role(settings[str(ctx.get_guild().id)])
        if not ctx.raw_options:
            embed = hikari.Embed(
                title=f"❌ Missing Identifier!",
                description=f"You either have to specify a Warn ID or a Member to delete Warns!",
                color=utils.Color.red().__str__(),
                timestamp=utils.get_time()
            )
            if ctx.interaction:
                await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
            else:
                await ctx.respond(embed=embed, delete_after=10)
        elif ctx.options.member and ctx.options.id:
            embed = hikari.Embed(
                title=f"⚠️ Missing Identifier!",
                description=f"You either have to specify a Mute ID or a Member to delete Warns!\nMember deletes all of the current Mutes from a Member,\nID only deletes one specifc Mute",
                color=utils.Color.orange().__str__(),
                timestamp=utils.get_time()
            )
            actionrow = ctx.bot.rest.build_action_row()
            actionrow.add_button(
                hikari.messages.ButtonStyle.PRIMARY,
                "ID-Button"
            ).set_label(f"ID").set_emoji("#️⃣").add_to_container()
            actionrow.add_button(
                hikari.messages.ButtonStyle.PRIMARY,
                "Member-Button"
            ).set_label(f"Member").set_emoji("👤").add_to_container()

            await ctx.respond(embed=embed, component=actionrow)
            try:
                event = await ctx.bot.wait_for(
                    hikari.InteractionCreateEvent,
                    timeout=60,
                    predicate=lambda e:
                    isinstance(e.interaction, hikari.ComponentInteraction)
                    and e.interaction.user.id == ctx.author.id
                    and e.interaction.guild_id == ctx.guild_id
                    and e.interaction.component_type == hikari.ComponentType.BUTTON
                    and e.interaction.channel_id == ctx.channel_id
                    and (e.interaction.custom_id == "Member-Button" or e.interaction.custom_id == "ID-Button")
                )
            except asyncio.TimeoutError:
                await ctx.edit_last_response("The menu timed out :c", components=[])
            else:
                if event.interaction.custom_id == "Member-Button":
                    embed = hikari.Embed(
                        title=f"✅ Deleted all Mutes from {ctx.options.member}",
                        color=utils.Color.green().__str__(),
                        timestamp=utils.get_time()
                    )

                    DBMute(mute_plugin.app.db).delete_all_mute_from(ctx.options.member.id, ctx.guild_id)
                    await on_mute_remove(ctx, ctx.options.member)
                    msg = await ctx.edit_last_response(embed=embed, components=[])

                else:
                    res = DBMute(mute_plugin.app.db).delete_mute(ctx.options.id)

                    if not res:
                        embed = hikari.Embed(
                            title=f"❌ ID Error!",
                            description=f"Your given ID: {ctx.options.id} does not belong to any active Mute!",
                            color=utils.Color.red().__str__(),
                            timestamp=utils.get_time()
                        )

                        msg = await ctx.edit_last_response(embed=embed, components=[])
                    else:
                        await on_mute_remove(ctx, user=ctx.get_guild().get_member(res[0][3]))
                        embed = hikari.Embed(
                            title=f"✅ Deleted Mutes with ID: {ctx.options.id}",
                            color=utils.Color.green().__str__(),
                            timestamp=utils.get_time()
                        )

                        msg = await ctx.edit_last_response(embed=embed, components=[])
                await asyncio.sleep(10)
                await msg.delete()
                return
        elif ctx.options.member:
            embed = hikari.Embed(
                title=f"✅ Deleted all Mutes from {ctx.options.member}",
                color=utils.Color.green().__str__(),
                timestamp=utils.get_time()
            )

            DBMute(mute_plugin.app.db).delete_all_mute_from(ctx.options.member.id, ctx.guild_id)
            await on_mute_remove(ctx, ctx.options.member)
            if ctx.interaction:
                return await ctx.respond(embed=embed, components=[], flags=hikari.MessageFlag.EPHEMERAL)
            else:
                return await ctx.respond(embed=embed, components=[], delete_after=5)
        else:
            res = DBMute(mute_plugin.app.db).delete_mute(ctx.options.id)
            res2 = DBMute(mute_plugin.app.db).get_mute(ctx.options.id)
            user = ctx.get_guild().get_member(res2[3])

            if not res:
                embed = hikari.Embed(
                    title=f"❌ ID Error!",
                    description=f"Your given ID: {ctx.options.id} does not belong to any active Mute!",
                    color=utils.Color.red().__str__(),
                    timestamp=utils.get_time()
                )

                if ctx.interaction:
                    return await ctx.respond(embed=embed, components=[], flags=hikari.MessageFlag.EPHEMERAL)
                else:
                    return await ctx.respond(embed=embed, components=[], delete_after=5)
            else:
                await on_mute_remove(ctx, user=ctx.get_guild().get_member(res[0][3]))
                embed = hikari.Embed(
                    title=f"✅ Deleted Mutes with ID: {ctx.options.id}",
                    color=utils.Color.green().__str__(),
                    timestamp=utils.get_time()
                )

                if ctx.interaction:
                    return await ctx.respond(embed=embed, components=[], flags=hikari.MessageFlag.EPHEMERAL)
                else:
                    return await ctx.respond(embed=embed, components=[], delete_after=5)


@mute.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("reason", "The Reason for kicking the Member", str, required=False)
@lightbulb.option("duration", "d=day,w=week,y=year,h=hour,m=minute | for example: 1d 2h", str, required=False)
@lightbulb.option("member", "The Member you want to mute", hikari.Member, required=True)
@lightbulb.command("add", "Mutes the given Member", inherit_checks=True)
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def mute_add(ctx: lightbulb.Context) -> None:
    if not ctx.interaction: await ctx.event.message.delete()
    async with ctx.get_channel().trigger_typing():
        duration = 0
        if ctx.options.duration:
            duration = utils.convert(ctx.options.duration)
            duration = int(time.time()) + duration
        if not type(duration) == int:
            embed = hikari.Embed(
                title=f"❌ Duration Error!",
                description=duration,
                color=utils.Color.red().__str__(),
                timestamp=utils.get_time()
            )
            if ctx.interaction:
                return await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
            else:
                return await ctx.respond(embed=embed, delete_after=5)
        reason = ctx.options.reason or f"No Reason provided by {ctx.author}"

        await _check(ctx)
        role = DBMute(ctx.app.db).get_mute_role(ctx.guild_id)[0]
        role = ctx.get_guild().get_role(role)
        try:
            await ctx.options.member.add_role(role=role, reason=f"{ctx.options.member} got Muted by {ctx.author}")
            id = DBMute(ctx.app.db).create_mute(ctx, reason, duration)
        except hikari.errors.ForbiddenError:
            embed = hikari.Embed(
                title=f"❌ Missing Permissions!",
                description=f"Does the Bot have the Permissions to Manage Roles or is the Role of the Bot above the Roles of the User you want to Mute?",
                color=utils.Color.red().__str__(),
                timestamp=utils.get_time()
            )
            if ctx.interaction:
                await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
            else:
                await ctx.respond(embed=embed, delete_after=5)
        else:
            embed = hikari.Embed(
                title=f"✅ {ctx.options.member} was sucessfully muted",
                description=f"Mute ID: {id}",
                color=utils.Color.green().__str__(),
                timestamp=utils.get_time()
            )
            if duration != 0: embed.add_field(name=f"Duration:", value=f"<t:{duration}:R>")
            if ctx.interaction:
                await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
            else:
                await ctx.respond(embed=embed, delete_after=20)


#TODO: Add a way to remove the Muterole when all mutes are removed!!!!

@mute_plugin.listener(hikari.RoleDeleteEvent)
async def on_delete(event: hikari.RoleDeleteEvent):
    r_id = event.role_id
    g_id = event.guild_id
    res = DBMute(mute_plugin.app.db).get_mute_role(g_id)
    if not res: return
    if r_id in res:
        guild: hikari.RESTGuild = await (await mute_plugin.app.rest.fetch_guild(g_id)).fetch_self()
        DBMute(mute_plugin.app.db).delete_mute_settings(g_id)
        DBMute(mute_plugin.app.db).delete_all_from_guild(g_id)
        owner = await mute_plugin.app.rest.fetch_user(guild.owner_id)
        try:
            embed = hikari.Embed(
                title=f"⚠️ Warning becouse of your Mute System!",
                description=f"In your Server {guild.name} was a Mute Role deleted! All Mutes are now deleted! To Setup a new Mute System just Mute someone or user /mute setup"
            )
            await owner.send("aaa")
        except hikari.errors.ForbiddenError:
            pass


@mute.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("setup", "Setup the Mute System.")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def mute_setup(ctx: lightbulb.Context):
    await _check(ctx)


@mute.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("member", "The Member you want to mute", hikari.Member, required=True)
@lightbulb.command("info", "Infos about the Mutes from a given Member", inherit_checks=True)
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def mutes_command(ctx: lightbulb.Context):
    async with ctx.get_channel().trigger_typing():
        await _check(ctx)
        if not ctx.interaction: await ctx.event.message.delete()
        member: hikari.Member = ctx.options.member
        res = DBMute(mute_plugin.app.db).get_all_for_user(user_id=member.id, guild_id=member.guild_id)
        embed = hikari.Embed(
            title=f'Member has no Mutes' if not len(res) > 0 else f"Mutes from {member.username}",
            color=utils.Color.red().__str__() if not len(res) > 0 else utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )
        for e, i in enumerate(res):
            auth = await mute_plugin.app.rest.fetch_user(i.author_id)
            embed.add_field(name=f"Mute {e + 1}", value=f"""ID: {i.unique_id}
            Ends: {f'<t:{i.time}:R>' if i.time > 0 else f'Forever, unless he gets unmuted!'}
            Reason: {i.reason}
            Muted by: {auth.username}
            """)
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=10)


@tasks.task(s=30, auto_start=True)
async def task():
    result = DBMute(mute_plugin.app.db).get_all()
    dic = {}
    for i in result:
        if str(i.guild_id) not in dic:
            dic[str(i.guild_id)] = [i]
        else:
            dic[str(i.guild_id)].append(i)

    mute_settigns = DBMute(mute_plugin.app.db).get_all_settings()

    dic2 = {}

    """
    dic2 -> {guildid:{user_id:{"muted":[bool],"class":class}}}
    """

    for e, i in dic.items():
        for x in i:
            if str(x.guild_id) not in dic2:
                dic2[str(x.guild_id)] = {str(x.user_id): {"muted": [x.isstillmuted], "class": x}}
            else:
                if str(x.user_id) not in dic2[str(x.guild_id)]:
                    dic2[str(x.guild_id)][str(x.user_id)] = {"muted": [x.isstillmuted], "class": x}
                else:
                    dic2[str(x.guild_id)][str(x.user_id)]["muted"].append(x.isstillmuted)

    for e, i in dic2.items():

        guild = await mute_plugin.app.rest.fetch_guild(int(e))
        guild = await guild.fetch_self()
        for x, h in i.items():
            mute: utils.mute_class = h["class"]
            member = await mute_plugin.app.rest.fetch_member(guild, mute.user_id)
            member_roles = [int(i) for i in member.role_ids]
            try:
                if mute_settigns[str(mute.guild_id)] in member_roles:
                    role = guild.get_role(mute_settigns[str(mute.guild_id)])
                    unmute: bool = False

                    for g in h["muted"]:
                        if not g:
                            if True not in h["muted"]:
                                unmute = True
                    if unmute:
                        await member.remove_role(role=role, reason=f"Unmuted")
                        DBMute(mute_plugin.app.db).delete_all_mute_from(mute.user_id, mute.guild_id)
                else:
                    DBMute(mute_plugin.app.db).delete_all_mute_from(mute.user_id, mute.guild_id)
            except KeyError:
                pass


def load(bot):
    bot.add_plugin(mute_plugin)


def unload(bot):
    bot.remove_plugin(mute_plugin)
