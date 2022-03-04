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
        await Log.send_error_log(event.exception, event.context.invoked_with)
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
        return await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.",
                                    delete_after=3)

    if isinstance(exception, lightbulb.errors.CommandNotFound):
        [print(i) for i in event.app.prefix_commands]
        return await event.context.respond(f"The Command {event.context.invoked_with} does not exist",delete_after=3)

    if isinstance(exception, lightbulb.NotOwner):
        return await event.context.respond("You are not the owner of this bot.",delete_after=3)

    if isinstance(exception, lightbulb.errors.BotMissingRequiredPermission):
        return await event.context.respond("The bot is missing one or more permissions required in order to run this command", delete_after=3)

    if isinstance(exception, lightbulb.errors.MissingRequiredPermission):
        return await event.context.respond("You are missing one or more permissions required in order to run this command", delete_after=3)

    await Log.send_error_log(event.exception,event.context.invoked_with)
    raise (event.exception)


def load(bot):
    bot.add_plugin(err_plugin)


def unload(bot):
    bot.remove_plugin(err_plugin)
