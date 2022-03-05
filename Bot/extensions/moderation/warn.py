import utils
from imports import *
from Bot.DataBase.warnsys import DBwarn


warn_plugin = lightbulb.Plugin("moderation.warn")




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


    event = utils.WarnEvent(
        app = ctx.app,
        author = ctx.author,
        user = user,
        reason = reason,
        guild_id = ctx.guild_id
    )

    warn_plugin.bot.dispatch(event)





def get_punishment(num:int,punishments:list):
    if num < punishments[0][0]:
        return None

    for e,i in enumerate(punishments):

        if num < i[0]:
            if e ==0:
                return None
            return punishments[e-1][1]
        if num >= punishments[len(punishments)-1][0]:
            return punishments[len(punishments)-1][1]


@warn_plugin.listener(utils.WarnEvent)
async def warn_event(event: utils.WarnEvent):
    result = DBwarn(event.app.db).get_warns(event.user)
    settings = DBwarn(event.app.db).get_settings(event.guild_id)
    if len(settings) == 0:
        DBwarn(event.app.db).add_settings(event.guild_id)
    settings = DBwarn(event.app.db).get_settings(event.guild_id)

    result = get_punishment(len(result),settings[str(event.guild_id)])


    if result:
        pass
        # TODO do punishment


def load(bot):
    bot.add_plugin(warn_plugin)


def unload(bot):
    bot.remove_plugin(warn_plugin)
