import hikari

import utils
from imports import *
from Bot.DataBase.warnsys import DBwarn
from Bot.extensions.moderation.ban import ban_member
from Bot.extensions.moderation.kick import kick_member
from Bot.DataBase.settings import DBSettings
warn_plugin = lightbulb.Plugin("moderation.warn")

async def event_mod_check(guild_id,member):
    result = DBSettings(warn_plugin.app.db).get_settings(guild_id)
    if not result: DBSettings(warn_plugin.app.db).add(guild_id)
    if not result: return False
    if not member: return False
    mod_roles = result[str(guild_id)][0]
    for i in member.role_ids:
        if int(i) in mod_roles:
            return True
    return False


@warn_plugin.listener(hikari.InteractionCreateEvent)
async def on_interaction(event:hikari.InteractionCreateEvent):
    if not isinstance(event.interaction, hikari.ComponentInteraction): return
    i = event.interaction
    if not i.guild_id: return
    if not i.member.permissions & hikari.permissions.Permissions.ADMINISTRATOR:
        if not await event_mod_check(i.guild_id, i.member): return
    if not i.custom_id.startswith("warn_delete"): return

    cid = i.custom_id.split(".")[1]

    res = DBwarn(warn_plugin.bot.db).del_warn(cid)
    if res:
        embed = hikari.Embed(
            title = f"✅ Deleted the Warn",
            description=f"Deleted Warn with ID: {cid}",
            color=utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )

        await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE,embed=embed,flags=hikari.MessageFlag.EPHEMERAL)
    else:
        embed = hikari.Embed(
            title=f"❌ ID Error!",
            description=f"Your given ID: {cid} does not belong to any Warn!",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )

        await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, embed=embed,
                                        flags=hikari.MessageFlag.EPHEMERAL)


@warn_plugin.command()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("warn","The Warnsystem")
@lightbulb.implements(lightbulb.PrefixCommandGroup,lightbulb.SlashCommandGroup)
async def mute_cmd(ctx):
    pass


@mute_cmd.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("member", "The User you want to have Info about", hikari.Member, required=True)
@lightbulb.command("info", "Infos About the Warns from a given User")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def warn_info(ctx:lightbulb.Context):
    embed = utils.l_embed
    if ctx.interaction:
        await ctx.respond(embed=embed,flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=10)
    member: hikari.Member = ctx.options.member
    if not ctx.interaction: await ctx.event.message.delete()
    res = DBwarn(ctx.app.db).get_warns(member.id,ctx.guild_id)
    embed = hikari.Embed(
        title=f'Member has no Warns' if not len(res) > 0 else f"Warns from {member.username}",
        color=utils.Color.red().__str__() if not len(res) > 0 else utils.Color.green().__str__(),
        timestamp=utils.get_time()
    )
    guild = ctx.get_guild()
    for e, i in enumerate(res):
        auth = guild.get_member(i[2])
        if not auth: auth = await warn_plugin.app.rest.fetch_user(i[2])
        embed.add_field(name=f"Warn {e + 1}", value=f"""Reason: {i[3]}
        Warned by: {auth.username}
        Warn ID: {i[5]}
        Zeit: <t:{i[4]}:R>
        """)
    rows = []
    for e, i in enumerate(res):
        index = math.floor(e/5)
        if index == len(rows): rows.append(ctx.bot.rest.build_action_row())
        act = rows[index]
        act.add_button(
            hikari.messages.ButtonStyle.PRIMARY,
            f"warn_delete.{i[5]}"
        ).set_label(f"{e+1}").set_emoji("💢").add_to_container()


    if ctx.interaction:
        await ctx.respond(embed=embed, components=rows,flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, components=rows, delete_after=10)




@mute_cmd.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("reason", "The Reason for warning the Member", str, required=True)
@lightbulb.option("member", "Warns the given Member", hikari.Member, required=True)
@lightbulb.command("add", "Warns the given Member")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand,lightbulb.MessageCommand)
async def warn(ctx: lightbulb.Context) -> None:
    if not ctx.interaction: await ctx.event.message.delete()
    if type(ctx) == lightbulb.context.UserContext:
        user = ctx.options.target
        reason = f"No Reason provided due to using User-Command"
    elif type(ctx) == lightbulb.context.MessageContext:
        user = ctx.options.target.author
        reason = f"Got warned trough following Message {ctx.options.target.content}"
    else:
        user = ctx.options.member
        reason = ctx.options.reason

    uni_id = DBwarn(ctx.app.db).add(ctx.author.id,reason,user.id,ctx.guild_id)

    warns = len(DBwarn(ctx.app.db).get_warns(user.id,ctx.guild_id))

    embed_sucessfull = hikari.Embed(
        title=f"Sucessfully warned the User `{user}` . He has now {warns} warns.",
        description=f"You can see the warns from a User with /warn info ...\nThe Warn ID is: {uni_id}",
        color=utils.Color.green().__str__(),
        timestamp=utils.get_time(),
    )

    embed_info = hikari.Embed(
        title=f"You got warned in the Guild `{ctx.get_guild().name}`! You have now {warns} warns!",
        color=utils.Color.red().__str__(),
        timestamp=utils.get_time(),
    )

    settings = DBwarn(ctx.app.db).get_settings(ctx.guild_id)
    next_punishment = get_next_punishment(warns,settings[str(ctx.guild_id)])

    if next_punishment:
        match next_punishment[1]:
            case "ban":
                punish = "banned"
            case "kick":
                punish = "kicked"
        embed_info.add_field("Next Punishment",f"When you will get warned {next_punishment[0]} more times, you will get **{punish}**")
    embed_info.set_thumbnail(utils.guild_icon(ctx.get_guild()))
    embed_info.add_field("Reason:",reason)

    if ctx.interaction:
        await ctx.respond(embed=embed_sucessfull,flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed_sucessfull, delete_after=3)


    await user.send(embed=embed_info)

    event = utils.WarnEvent(
        app = ctx.app,
        author = ctx.author,
        user = user,
        reason = reason,
        guild_id = ctx.guild_id,
        guild = ctx.get_guild()
    )

    warn_plugin.bot.dispatch(event)


@mute_cmd.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("id","The Warn-ID from the Warn you want to delete!", required=False)
@lightbulb.option("member", "The Member you want to delete the Warns from", hikari.Member, required=False)
@lightbulb.command("delete", "Deletes The Warns from a given Member or from Warn-ID",inherit_checks=True)
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def mute_delete(ctx:lightbulb.Context):
    async with ctx.get_channel().trigger_typing():
        if not ctx.interaction: await ctx.event.message.delete()
        if 'delete' in ctx.raw_options: del ctx.raw_options['delete']
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
                description=f"You either have to specify a Warn ID or a Member to delete Warns!\nMember deletes all of the current Warns from a Member,\nID only deletes one specifc Warn",
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

            if ctx.interaction:
                await ctx.respond(embed=embed,component=actionrow, flags=hikari.MessageFlag.EPHEMERAL)
            else:
                await ctx.respond(embed=embed,component=actionrow,delete_after=60)
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
                if ctx.interaction:
                    await ctx.respond("The menu timed out :c",flags=hikari.MessageFlag.EPHEMERAL)
                else:
                    await ctx.edit_last_response("The menu timed out :c", delete_after=5)
            else:
                msg=None
                if event.interaction.custom_id == "Member-Button":
                    embed = hikari.Embed(
                        title=f"✅ Deleted all Warns from {ctx.options.member}",
                        color=utils.Color.green().__str__(),
                        timestamp=utils.get_time()
                    )
                    DBwarn(warn_plugin.app.db).delete_all_mute_from(ctx.options.member.id, ctx.guild_id)
                    if ctx.interaction:
                        await event.interaction.create_initial_response(hikari.ResponseType.MESSAGE_CREATE,embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
                    else:
                        msg = await ctx.edit_last_response(embed=embed, components=[])

                else:
                    res = DBwarn(warn_plugin.app.db).del_warn(ctx.options.id)
                    if not res:
                        embed = hikari.Embed(
                            title=f"❌ ID Error!",
                            description=f"Your given ID: {ctx.options.id} does not belong to any active Warn!",
                            color=utils.Color.red().__str__(),
                            timestamp=utils.get_time()
                        )
                        if ctx.interaction:
                            await event.interaction.create_initial_response(hikari.ResponseType.MESSAGE_CREATE,
                                                                            embed=embed,
                                                                            flags=hikari.MessageFlag.EPHEMERAL)
                        else:
                            msg = await ctx.edit_last_response(embed=embed, components=[])

                    else:
                        embed = hikari.Embed(
                            title=f"✅ Deleted Warns with ID: {ctx.options.id}",
                            color=utils.Color.green().__str__(),
                            timestamp=utils.get_time()
                        )

                        if ctx.interaction:
                            await event.interaction.create_initial_response(hikari.ResponseType.MESSAGE_CREATE,
                                                                            embed=embed,
                                                                            flags=hikari.MessageFlag.EPHEMERAL)
                        else:
                            msg = await ctx.edit_last_response(embed=embed, components=[])
                if msg:
                    await asyncio.sleep(10)
                    await msg.delete()
                    return
        elif ctx.options.member:
            embed = hikari.Embed(
                title=f"✅ Deleted all Warns from {ctx.options.member}",
                color=utils.Color.green().__str__(),
                timestamp=utils.get_time()
            )
            DBwarn(warn_plugin.app.db).delete_all_mute_from(ctx.options.member.id, ctx.guild_id)

            if ctx.interaction:
                return await ctx.respond(embed=embed, components=[], flags=hikari.MessageFlag.EPHEMERAL)
            else:
                return await ctx.respond(embed=embed, components=[],delete_after=5)
        else:
            res = DBwarn(warn_plugin.bot.db).del_warn(ctx.options.id)
            if not res:
                embed = hikari.Embed(
                    title=f"❌ ID Error!",
                    description=f"Your given ID: {ctx.options.id} does not belong to any active Warn!",
                    color=utils.Color.red().__str__(),
                    timestamp=utils.get_time()
                )

                if ctx.interaction:
                    return await ctx.respond(embed=embed, components=[], flags=hikari.MessageFlag.EPHEMERAL)
                else:
                    return await ctx.respond(embed=embed, components=[],delete_after=5)
            else:
                embed = hikari.Embed(
                    title=f"✅ Deleted Warns with ID: {ctx.options.id}",
                    color=utils.Color.green().__str__(),
                    timestamp=utils.get_time()
                )

                if ctx.interaction:
                    return await ctx.respond(embed=embed, components=[], flags=hikari.MessageFlag.EPHEMERAL)
                else:
                    return await ctx.respond(embed=embed, components=[],delete_after=5)

def get_next_punishment(num,punishments):
    if len(punishments) == 0:
        return None
    if num > punishments[len(punishments)-1][0]:
        return [0,punishments[len(punishments)-1][1]]

    before = None
    for e,i in enumerate(punishments):
        if not before:
            if num < i[0]:
                return [i[0]-num,i[1]]
        if num == i[0]:
            return [0,i[1]]
        elif num < i[0]:
            return [i[0]-num,i[1]]

    return [0,punishments[len(punishments)-1][1]]



def get_punishment(num:int,punishments:list) -> None | str:
    if num < punishments[0][0]:
        return None

    if num > punishments[len(punishments)-1][0]:
        return punishments[len(punishments)-1][1]
    else:
        for i in punishments:
            if i[0] == num:
                return i[1]


@warn_plugin.listener(utils.WarnEvent)
async def warn_event(event: utils.WarnEvent):
    result = DBwarn(event.app.db).get_warns(event.user,event.guild_id)
    settings = DBwarn(event.app.db).get_settings(event.guild_id)
    if len(settings) == 0:
        DBwarn(event.app.db).add_settings(event.guild_id)

    settings = DBwarn(event.app.db).get_settings(event.guild_id)
    if len(settings[str(event.guild_id)]) == 0:
        return

    punishment = get_punishment(len(result),settings[str(event.guild_id)])

    done = None

    if punishment:
        match punishment:
            case "ban":
                res = f"{event.user} got banned becouse he has now {len(result)} warns."
                await ban_member(event.user,event.guild,res)
                done = "banned"
            case "kick":
                res = f"{event.user} got kicked becouse he has now {len(result)} warns."
                await kick_member(event.user, event.guild, res)
                done = "kicked"
            ## TODO add more punishments when the system for that is finished.
    if done:
        embed = hikari.Embed(
            title=f"You got {done} from `{event.guild.name}`, becouse you got warned {len(result)} times.",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )
        embed.set_thumbnail(utils.guild_icon(event.guild))
        await event.user.send(embed=embed)

def load(bot):
    bot.add_plugin(warn_plugin)


def unload(bot):
    bot.remove_plugin(warn_plugin)
