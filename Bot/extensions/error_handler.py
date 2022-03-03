import discord
from imports import *
from Bot import __prefix__, Logger


err_plugin = lightbulb.Plugin("error_plugin")


Log = Logger()

@err_plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event):
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(
            f"Something went wrong during invocation of command `{event.context.command.name}`.",
            delete_after=3
        )
        await Log.send_error_log(event.exception, event.context.command.name)
        raise event.exception

    exception = event.exception.__cause__ or event.exception

    if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
        if isinstance(event.context, lightbulb.context.prefix.PrefixContext):
            if event.context.invoked_with == "clear":
                return await event.context.respond(
                    f"Please specify the number of messages to clear `e.g. {__prefix__}clear 10`",
                    delete_after=3
                )

    if isinstance(event.exception, lightbulb.errors.OnlyInGuild):
        return await event.context.respond(
            f"This Command can only be used in Guilds! Sorry \:(",
            delete_after=3
        )

    if isinstance(exception, lightbulb.NotOwner):
        return await event.context.respond("You are not the owner of this bot.", delete_after=3)

    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.",
                                    delete_after=3)

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("You are not the owner of this bot.")

    await Log.send_error_log(event.exception, event.context.command.name)
    raise (event.exception)


def load(bot):
    bot.add_plugin(err_plugin)


def unload(bot):
    bot.remove_plugin(err_plugin)
