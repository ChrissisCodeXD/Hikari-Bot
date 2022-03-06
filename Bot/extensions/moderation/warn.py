import utils
from imports import *
from Bot.DataBase.warnsys import DBwarn
from Bot.extensions.moderation.ban import ban_member
from Bot.extensions.moderation.kick import kick_member
warn_plugin = lightbulb.Plugin("moderation.warn")



@warn_plugin.command()
@lightbulb.option("reason", "The Reason for warning the Member", str, required=True)
@lightbulb.option("member", "Warns the given Member", hikari.Member, required=True)
@lightbulb.command("warn_info", "Warns the given Member")

@lightbulb.implements(lightbulb.UserCommand, lightbulb.SlashCommand, lightbulb.PrefixCommand, lightbulb.MessageCommand)




@warn_plugin.command()
@lightbulb.option("reason", "The Reason for warning the Member", str, required=True)
@lightbulb.option("member", "Warns the given Member", hikari.Member, required=True)
@lightbulb.command("warn", "Warns the given Member")
@lightbulb.implements(lightbulb.UserCommand, lightbulb.SlashCommand, lightbulb.PrefixCommand, lightbulb.MessageCommand)
async def warn(ctx: lightbulb.Context) -> None:

    if type(ctx) == lightbulb.context.UserContext:
        user = ctx.options.target
        reason = f"No Reason provided due to using User-Command"
    elif type(ctx) == lightbulb.context.MessageContext:
        user = ctx.options.target.author
        reason = f"Got warned trough following Message {ctx.options.target.content}"
    else:
        user = ctx.options.member
        reason = ctx.options.reason

    DBwarn(ctx.app.db).add(ctx.author.id,reason,user.id,ctx.guild_id)

    warns = len(DBwarn(ctx.app.db).get_warns(user.id))

    embed_sucessfull = hikari.Embed(
        title=f"Sucessfully warned the User `{user}` . He has now {warns} warns.",
        description=f"You can see the warns from a User with /warns ...",
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
    result = DBwarn(event.app.db).get_warns(event.user)
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
