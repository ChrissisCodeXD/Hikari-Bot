import hikari
import lightbulb

from imports import *
from Bot.DataBase.auto_role import DBRole

auto_role_plugin = lightbulb.Plugin("server_managment-managment.auto_roles")

auto_role_plugin.add_checks(
    lightbulb.checks.guild_only,
)


@auto_role_plugin.command()
@lightbulb.command('auto_role', 'The Auto Role System')
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def role(ctx):
    pass


@role.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("role", "The role to add to the user when he joins the server", type=hikari.Role, required=True)
@lightbulb.command('add_role', 'Add a role to the System')
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def add_role(ctx):
    role: hikari.Role = ctx.options.role

    res = DBRole(ctx.app.db).add_role(ctx.guild_id, role.id)
    if not res:
        embed = hikari.Embed(title="Role Already Exists",
                             description="The role you are trying to add already exists in the system",
                             color=utils.Color.red().__str__(), timestamp=utils.get_time())

        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
    else:
        embed = hikari.Embed(title="Role Added",
                             description=f"The role {role.mention} has been added to the system",
                             color=utils.Color.green().__str__(), timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)


@role.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command('get_roles', 'Get all the roles in the system')
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def get_roles(ctx):
    roles = DBRole(ctx.app.db).get_auto_roles(ctx.guild_id)
    if roles:
        roles = [ctx.get_guild().get_role(role) for role in roles]
        embed = hikari.Embed(title="Roles",
                             description="\n".join([f"{role.mention}" for role in roles]),
                             color=utils.Color.green().__str__(), timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
    else:
        embed = hikari.Embed(title="No Roles",
                             description="There are no roles in the system",
                             color=utils.Color.red().__str__(), timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)


@role.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("role", "The role to remove from the system", type=hikari.Role, required=True)
@lightbulb.command('remove_role', 'Remove a role from the system')
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def remove_role(ctx):
    role: hikari.Role = ctx.options.role

    res = DBRole(ctx.app.db).remove_role(ctx.guild_id, role.id)
    if not res:
        embed = hikari.Embed(title="Role Not Found",
                             description="The role you are trying to remove does not exist in the system",
                             color=utils.Color.red().__str__(), timestamp=utils.get_time())

        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
    else:
        embed = hikari.Embed(title="Role Removed",
                             description=f"The role {role.mention} has been removed from the system",
                             color=utils.Color.green().__str__(), timestamp=utils.get_time())
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)


@role.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command('clear_roles', 'Deletes all the roles in the system')
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def clear_roles(ctx):
    res = DBRole(ctx.app.db).delete_all_from_guild(ctx.guild_id)

    embed = hikari.Embed(title="Roles Cleared",
                         description="All the roles have been cleared from the system",
                         color=utils.Color.green().__str__(), timestamp=utils.get_time())
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=5)


@auto_role_plugin.listener(hikari.events.MemberCreateEvent)
async def on_member_create(event: hikari.events.MemberCreateEvent):
    roles = DBRole(event.app.db).get_auto_roles(event.guild_id)
    if roles:
        roles = [event.get_guild().get_role(role) for role in roles]
        for role in roles:
            await event.member.add_role(role)


def load(bot):
    bot.add_plugin(auto_role_plugin)


def unload(bot):
    bot.remove_plugin(auto_role_plugin)
