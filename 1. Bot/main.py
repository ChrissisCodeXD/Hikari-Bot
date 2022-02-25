import hikari
import lightbulb

from imports import *


bot: lightbulb.BotApp = lightbulb.BotApp(prefix=lightbulb.app.when_mentioned_or("!"), token=env().get('TOKEN1'), intents=hikari.Intents.ALL)



@bot.command()
@lightbulb.command("ping", "Checks that the bot is alive")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")


@bot.command()
@lightbulb.option("num2", "Second number", int)
@lightbulb.option("num1", "First number", int)
@lightbulb.command("add", "Adds the two given numbers together")
@lightbulb.implements(lightbulb.PrefixCommand,lightbulb.SlashCommand)
async def add(ctx: lightbulb.Context) -> None:
    """Adds the two given numbers together"""
    num1, num2 = ctx.options.num1, ctx.options.num2
    await ctx.respond(f"{num1} + {num2} = {num1 + num2}")


@bot.command()
@lightbulb.option("user", "User to greet", hikari.User)
@lightbulb.command("greet", "Greets the specified user")
@lightbulb.implements(lightbulb.PrefixCommand,lightbulb.SlashCommand)
async def greet(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Hello {ctx.options.user.mention}!")




bot.run()
