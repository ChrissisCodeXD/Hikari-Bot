import lightbulb

from imports import *
from Bot.DataBase.mutesys import DBMute

owner_plugin = lightbulb.Plugin("owner.owner_plugin")
owner_plugin.add_checks(
    lightbulb.checks.guild_only,
    lightbulb.checks.owner_only
)
log = logging.getLogger(__name__)
from Bot import __beta__

_extensions = [p.stem for p in Path("./extensions/").glob("*.py")]
_extensions.extend([f"moderation.{p.stem}" for p in Path("./extensions/moderation/").glob("*.py")])
_extensions.extend([f"events.{p.stem}" for p in Path("./extensions/events/").glob("*.py")])
_extensions.extend([f"settings.{p.stem}" for p in Path("./extensions/settings/").glob("*.py")])
_extensions.extend([f"test.{p.stem}" for p in Path("./extensions/test/").glob("*.py")])
_extensions.extend([f"fun.{p.stem}" for p in Path("./extensions/fun/").glob("*.py")])
_extensions.extend([f"server_managment.{p.stem}" for p in Path("./extensions/server_managment/").glob("*.py")])

extensions = []
for i in _extensions:
    if not i.split(".")[0] in extensions:
        extensions.append(i.split(".")[0])


@owner_plugin.command()
@lightbulb.command("shutdown", "Shutds down the Bot.", guilds=[948904191559077888])
@lightbulb.implements(lightbulb.SlashCommand)
async def mute(ctx: lightbulb.Context) -> None:
    log.info("Shutdown signal received")
    await ctx.respond("Now shutting down.", flags=hikari.MessageFlag.EPHEMERAL)
    await ctx.bot.close()


@owner_plugin.command()
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command("error", "Reload the Bot")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def error(ctx: lightbulb.Context):
    raise RuntimeError("This is a test error")


@owner_plugin.command()
@lightbulb.option("globals", "Whether or not to purge global slash commands from the bot.", bool, required=True,
                  default=False)
@lightbulb.option("guild", "The ID of the target guild", str, required=True)
@lightbulb.command("clearcmd", "purge all slash commands from specified guild")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def purge_cmd(ctx: lightbulb.Context):
    guild = ctx.options.guild
    globals = ctx.options.globals
    await ctx.bot.purge_application_commands(guild, global_commands=globals)
    await ctx.respond("Task Completed Successfully!")


@owner_plugin.command()
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command("extension", "manage an extension")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def extension_manager(ctx: lightbulb.Context):
    pass


@extension_manager.child()
@lightbulb.option("name", "the extension you want to reload", str, required=True,
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("category", "the category of the extension", str, required=False,
                  choices=extensions)
@lightbulb.command("reload", "Reload an extension", inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def extension_reload(ctx: lightbulb.Context):
    name = ctx.options.name
    category = ctx.options.category
    if category:
        ctx.bot.reload_extensions(f"Bot.extensions.{category}.{name}")
    else:
        ctx.bot.reload_extensions(f"Bot.extensions.{name}")
    if ctx.interaction:
        await ctx.respond(f"Successfully reloaded `{name}`!", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(f"Successfully reloaded `{name}`!", delete_after=20)


@extension_manager.child()
@lightbulb.option("name", "the extension you want to unload", str, required=True,
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("category", "the category of the extension", str, required=False,
                  choices=extensions)
@lightbulb.command("unload", "Unload an extension", inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def extension_unload(ctx: lightbulb.Context):
    name = ctx.options.name
    category = ctx.options.category
    if category:
        ctx.bot.unload_extensions(f"Bot.extensions.{category}.{name}")
    else:
        ctx.bot.unload_extensions(f"Bot.extensions.{name}")
    if ctx.interaction:
        await ctx.respond(f"Successfully unloaded `{name}`!", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(f"Successfully unloaded `{name}`!", delete_after=20)


@extension_manager.child()
@lightbulb.option("name", "the extension you want to load", str, required=True,
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("category", "the category of the extension", str, required=False,
                  choices=extensions)
@lightbulb.command("load", "Load an extension", inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def extension_load(ctx: lightbulb.Context):
    name = ctx.options.name
    category = ctx.options.category
    if category:
        ctx.bot.load_extensions(f"Bot.extensions.{category}.{name}")
    else:
        ctx.bot.load_extensions(f"Bot.extensions.{name}")

    if ctx.interaction:
        await ctx.respond(f"Successfully loaded `{name}`!", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(f"Successfully loaded `{name}`!", delete_after=20)


def load(bot):
    bot.add_plugin(owner_plugin)


def unload(bot):
    bot.remove_plugin(owner_plugin)
