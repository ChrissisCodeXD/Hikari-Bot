import lightbulb
from Bot.DataBase.settings import DBSettings


async def mod_check(ctx: lightbulb.Context):
    result = DBSettings(ctx.app.db).get_settings(ctx.guild_id)
    if not result: DBSettings(ctx.app.db).add(ctx.guild_id)
    if not result: return False
    if not ctx.member: return False
    mod_roles = result[str(ctx.guild_id)][0]
    for i in ctx.member.role_ids:
        if int(i) in mod_roles:
            return True
    return False


async def mod_check_without_ctx(bot, guild_id, member):
    result = DBSettings(bot.db).get_settings(guild_id)
    if not result: DBSettings(bot.db).add(guild_id)
    if not result: return False
    if not member: return False
    mod_roles = result[str(guild_id)][0]
    for i in member.role_ids:
        if int(i) in mod_roles:
            return True
    return False
