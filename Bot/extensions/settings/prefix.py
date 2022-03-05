from imports import *
from Bot.bot import Prefixes

prefix_plugin = lightbulb.Plugin("settings.prefix")

prefix_plugin.add_checks(
    lightbulb.checks.guild_only,
    lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR),
)


@prefix_plugin.command()
@lightbulb.option("prefix", "The new Prefix", str)
@lightbulb.command("change_prefix", "This Commands lets you change your Current Prefix for Commands!")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def _prefix_cmd(ctx: lightbulb.Context) -> None:
    prefix = ctx.options.prefix
    ctx.app._prefix__get_class.change_prefix(ctx.guild_id, prefix)
    embed = hikari.Embed(title=f"Changed the Prefix to ` {prefix} `",
                         description=f"Now you can use every normal Command with `{prefix}command_name`",
                         color=utils.Color.green().__str__())
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed)


@prefix_plugin.command()
@lightbulb.command("get_prefix", "With this Command you can check which prefix you have")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def _prefix_cmd(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title=f"Your Current Prefix ist ` {prefix_plugin.app._prefix__get_class.get_prefix(ctx.guild_id)} `",
        color=utils.Color.green().__str__())
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed)


def load(bot):
    bot.add_plugin(prefix_plugin)


def unload(bot):
    bot.remove_plugin(prefix_plugin)
