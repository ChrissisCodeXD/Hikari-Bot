import hikari
import lightbulb

import utils
from imports import *
from Bot.DataBase.levelsys import DBLevel



buttons = {
    "ison": ["Activate Level System", "Deactivate Level System"],
    "doubleexp": ["Activate Double Exp", "Deactivate Double Exp"],
}


async def build_setting_rows(bot,settings):
    rows: t.list[lightbulb.ActionRow] = []
    row = bot.rest.build_action_row()


    for i, button in enumerate(settings):
        if i % 5 == 0 and i != 0:
            rows.append(row)
            row = bot.rest.build_action_row()

        label = buttons.get(button)
        if not label: continue

        if settings[button] == 0:
            label = label[0]
        else:
            label = label[1]

        (
            row.add_button(
                hikari.ButtonStyle.SUCCESS if settings[button] == 0 else hikari.ButtonStyle.DANGER,
                button
            )
            .set_label(label)
            .set_emoji("✅" if settings[button] == 0 else "⛔")
            .add_to_container()
        )
    rows.append(row)

    row = bot.rest.build_action_row()


    select = row.add_select_menu("change_exp_multiplier")
    select.set_placeholder("Select Exp Multiplier")

    select.add_option("0.25", "0.25").set_description("25% of the Normal Exp").set_emoji("➡").add_to_menu()
    select.add_option("0.5", "0.5").set_description("50% of the Normal Exp").set_emoji("➡").add_to_menu()
    select.add_option("0.75", "0.75").set_description("75% of the Normal Exp").set_emoji("➡").add_to_menu()
    select.add_option("1", "1").set_description("Normal Exp").set_emoji("➡").add_to_menu()
    select.add_option("1.25", "1.25").set_description("125% of the Normal Exp").set_emoji("➡").add_to_menu()
    select.add_option("1.5", "1.5").set_description("150% of the Normal Exp").set_emoji("➡").add_to_menu()
    select.add_option("1.75", "1.75").set_description("175% of the Normal Exp").set_emoji("➡").add_to_menu()
    select.add_option("2", "2").set_description("200% of the Normal Exp").set_emoji("➡").add_to_menu()
    select.add_to_container()

    rows.append(row)

    return rows







level_plugin = lightbulb.Plugin("fun.level")


def checknewlvl( authorid, guildid):
    return (DBLevel(level_plugin.app.db).checkLVL(authorid, guildid))


@level_plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent):
    if event.member.is_bot: return
    exp = random.randint(10, 25)
    res = DBLevel(event.app.db).isindatabaseguilds(event.get_guild().id)
    if not res:
        DBLevel(event.app.db).addtoguilds(event.get_guild().id)
    settings = DBLevel(event.app.db).get_settings(event.get_guild().id)
    if not settings: return
    if settings["ison"] == 0: return

    exp = exp * settings["xpmult"]
    if settings["doubleexp"] == 1:
        exp = exp * 2


    res = DBLevel(event.app.db).isindatabase(event.member.id, event.guild_id)

    if not res:
        DBLevel(event.app.db).add(event.member.id, exp, event.get_guild().id, event.member.username,
                                  str(event.member.make_avatar_url()))
        return

    if not (int(time.time()) - int(datetime.datetime.timestamp(res[3]))) > 60: return

    print('new_exp')

    DBLevel(event.app.db).addEXP(event.member.id, event.get_guild().id, exp)

    newlvl = checknewlvl(event.member.id, event.get_guild().id)
    if newlvl:
        channels = DBLevel(event.app.db).getlvlupchannels(event.guild_id)
        for i in channels:
            channel = event.get_guild().get_channel(i)
            await channel.send(
                f"{event.member.mention} has leveled up to lvl {newlvl}!")


@level_plugin.command()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("level","the level system")
@lightbulb.implements(lightbulb.PrefixCommandGroup,lightbulb.SlashCommandGroup)
async def level(self,ctx):
    pass


@level.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("channels","see all the levelup channels")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def channels(ctx):
    res = DBLevel(ctx.app.db).getlvlupchannels(ctx.guild_id)
    if not res:
        embed = hikari.Embed(title="❌ Error",description="No channels set",color=utils.Color.red().__str__(),timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
        return
    embed = hikari.Embed(title="✅ Levelup-Channels",
                         description="\n".join([ctx.get_guild().get_channel(i).mention for i in res]),
                         color=utils.Color.green().__str__(),timestamp=utils.get_time())
    if ctx.interaction:
        await ctx.respond(embed=embed,flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed,delete_after=5)


@level.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("channel","the channel to add",type=hikari.TextableGuildChannel,required=True)
@lightbulb.command("setchannel","set a levelup channel")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def setchannel(ctx):
    res = DBLevel(ctx.app.db).getlvlupchannels(ctx.guild_id)
    channel = ctx.options.channel
    if channel.id in res:
        embed = hikari.Embed(title="❌ Error",
                             description="This channel is already set",
                             color=utils.Color.red().__str__(),timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
        return
    DBLevel(ctx.app.db).add_lvlup_channel(ctx.guild_id,channel.id)
    embed = hikari.Embed(title="✅ Success",
                         description=f"{ctx.get_guild().get_channel(channel.id).mention} has been added to the levelup channels",
                         color=utils.Color.green().__str__(),timestamp=utils.get_time())
    if ctx.interaction:
        await ctx.respond(embed=embed,flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed,delete_after=5)
    return


@level.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("channel","the channel to remove",type=hikari.TextableGuildChannel,required=True)
@lightbulb.command("removechannel","remove a levelup channel")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def removechannel(ctx):
    res = DBLevel(ctx.app.db).getlvlupchannels(ctx.guild_id)
    channel = ctx.options.channel
    if channel.id not in res:
        embed = hikari.Embed(title="❌ Error",
                             description="This channel is not set",
                             color=utils.Color.red().__str__(),timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
        return
    DBLevel(ctx.app.db).remove_lvlup_channels(ctx.guild_id,channel.id)
    embed = hikari.Embed(title="✅ Success",
                         description=f"{ctx.get_guild().get_channel(channel.id).mention} has been removed from the levelup channels",
                         color=utils.Color.green().__str__(),timestamp=utils.get_time())
    if ctx.interaction:
        await ctx.respond(embed=embed,flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed,delete_after=5)
    return



@level.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("settings","settings for levelsystem")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def settings(ctx):
    settings = DBLevel(ctx.app.db).get_settings(ctx.guild_id)
    if not settings:
        embed = hikari.Embed(title="❌ Error",
                             description="There are no settings for this server",
                             color=utils.Color.red().__str__(),timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
        return
    embed = hikari.Embed(title="Level Settings",
                         color=utils.Color.green().__str__(),timestamp=utils.get_time())
    levelup_channels = "\n".join([ctx.get_guild().get_channel(x).name for x in settings["channels"]])
    embed.add_field("Levelsysten Status","```✅ - on```" if settings["ison"] == 1 else "```❌ - off```",inline=True)
    embed.add_field("XP Multiplier","```{}```".format(settings["xpmult"]),inline=True)
    embed.add_field("Double XP","```✅ - on```" if settings["doubleexp"] == 1 else "```❌ - off```",inline=True)
    embed.add_field("Levelup Channels","```{}```".format(levelup_channels) if levelup_channels else "```❌ - empty```",inline=True)
    #TODO: add levelup Message
    #embed.add_field("Levelup Message","```{}```".format(settings["levelup_message"]) if settings["levelup_message"] else "```❌ - empty```")

    rows = await build_setting_rows(ctx.app,settings)


    await ctx.respond(embed=embed,components=rows)






@level.child()
@lightbulb.command("help","help for levelsystem")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def help(ctx):
    embed = hikari.Embed(title="✅ Level System Help",
                         description="This is the help for the level system",
                         color=utils.Color.green().__str__())
    embed.add_field("How does it work?",
                    "When a User sends a Message, he gets XP. When he reaches a certain amount of XP, he gets a message in the levelup channel and levels up.\n"
                    "By Default there is a 60 second Cooldown before you get XP again. This means that a User can spam as much as he wants, but only gets XP every 60 seconds."
                    "You can change this with the level Cooldown command.\n"
                    "```/level cooldown <seconds>```",inline=False)
    embed.add_field("How do I add a levelup channel?",
                    "```/level addchannel <channel>```",inline=False)
    embed.add_field("How do I remove a levelup channel?",
                    "```/level removechannel <channel>```",inline=False)
    embed.add_field("The Level Settings",
                    "```/level settings```\n"
                    "You can change the settings for the level system here.\n"
                    "By clicking on the Level System Button you can either turn it on or off.\n"
                    "By clicking on the Double XP Button you can either turn it on or off.\n"
                    "You can also Select a Custom Exp Multiplier by clicking on `Select Exp Multiplier` and choosing the wanted Multiplier\n"
                    ,inline=False)

    embed2 = hikari.Embed(color=utils.Color.green().__str__())
    embed2.set_image("https://cdn.discordapp.com/attachments/948961120662728724/960141932754001981/unknown.png")

    if ctx.interaction:
        await ctx.respond(embeds=[embed,embed2],flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embeds=[embed,embed2],delete_after=5)




@level_plugin.listener(hikari.events.InteractionCreateEvent)
async def on_interaction_create(event:hikari.events.InteractionCreateEvent):
    e = event
    if isinstance(e.interaction, hikari.ComponentInteraction):
        i: hikari.ComponentInteraction = e.interaction

        if not i.guild_id: return
        if i.custom_id in buttons:
            res = utils.mod_check_without_ctx(e.app,i.guild_id,i.member)
            if not res or not i.member.permissions & hikari.Permissions.ADMINISTRATOR:
                embed = hikari.Embed(title="❌ Error",
                                     description="You are not allowed to use this",
                                     color=utils.Color.red().__str__(),timestamp=utils.get_time())
                await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE,embed=embed,flags=hikari.MessageFlag.EPHEMERAL)
                return
            else:
                settings = DBLevel(e.app.db).get_settings(i.guild_id)
                if i.custom_id in buttons:
                    old_value = settings[i.custom_id]

                    new_value = "abcdefghijklmnopqrstuvwxyz"
                    match old_value:
                        case 0:
                            new_value = 1
                        case 1:
                            new_value = 0
                    if new_value == "abcdefghijklmnopqrstuvwxyz": return
                    DBLevel(e.app.db).update_settings(i.guild_id,i.custom_id,new_value)
                    settings = DBLevel(e.app.db).get_settings(i.guild_id)
                    embed = hikari.Embed(title="✅ Success",
                                         description="The setting have been updated",
                                         color=utils.Color.green().__str__(),timestamp=utils.get_time())
                    embed.add_field(f"Updated: {i.custom_id}",
                                    f"``` {'❌ - off' if new_value == 0 else '✅ - on'}```",
                                    inline=True)
                    await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE,embed=embed,flags=hikari.MessageFlag.EPHEMERAL)

                    embed = hikari.Embed(title="Level Settings",
                                         color=utils.Color.green().__str__(), timestamp=utils.get_time())
                    levelup_channels = "\n".join([i.get_guild().get_channel(x).name for x in settings["channels"]])
                    embed.add_field("Levelsysten Status", "```✅ - on```" if settings["ison"] == 1 else "```❌ - off```",
                                    inline=True)
                    embed.add_field("XP Multiplier", "```{}```".format(settings["xpmult"]), inline=True)
                    embed.add_field("Double XP", "```✅ - on```" if settings["doubleexp"] == 1 else "```❌ - off```",
                                    inline=True)
                    embed.add_field("Levelup Channels",
                                    "```{}```".format(levelup_channels) if levelup_channels else "```❌ - empty```",
                                    inline=True)

                    rows = await build_setting_rows(e.app,settings)

                    await i.message.edit(embed=embed,components=rows)
        elif i.custom_id == "change_exp_multiplier":
            res = utils.mod_check_without_ctx(e.app, i.guild_id, i.member)
            if not res or not i.member.permissions & hikari.Permissions.ADMINISTRATOR:
                embed = hikari.Embed(title="❌ Error",
                                     description="You are not allowed to use this",
                                     color=utils.Color.red().__str__(), timestamp=utils.get_time())
                await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, embed=embed,
                                                flags=hikari.MessageFlag.EPHEMERAL)
                return
            else:
                new_mult = i.values[0]
                new_mult = float(new_mult)
                DBLevel(e.app.db).update_settings(i.guild_id, "xpmult", new_mult)
                settings = DBLevel(e.app.db).get_settings(i.guild_id)
                embed = hikari.Embed(title="✅ Success",
                                     description="The settings have been updated",
                                     color=utils.Color.green().__str__(), timestamp=utils.get_time())
                embed.add_field(f"Updated: XP Multiplier",
                                f"```{new_mult}```",
                                inline=True)
                await i.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, embed=embed,
                                                                flags=hikari.MessageFlag.EPHEMERAL)
                embed = hikari.Embed(title="Level Settings",
                                     color=utils.Color.green().__str__(), timestamp=utils.get_time())
                levelup_channels = "\n".join([i.get_guild().get_channel(x).name for x in settings["channels"]])
                embed.add_field("Levelsysten Status", "```✅ - on```" if settings["ison"] == 1 else "```❌ - off```",
                                inline=True)
                embed.add_field("XP Multiplier", "```{}```".format(settings["xpmult"]), inline=True)
                embed.add_field("Double XP", "```✅ - on```" if settings["doubleexp"] == 1 else "```❌ - off```",
                                inline=True)
                embed.add_field("Levelup Channels",
                                "```{}```".format(levelup_channels) if levelup_channels else "```❌ - empty```",
                                inline=True)

                rows = await build_setting_rows(e.app,settings)

                await i.message.edit(embed=embed,components=rows)




def load(bot):
    bot.add_plugin(level_plugin)


def unload(bot):
    bot.remove_plugin(level_plugin)
