import hikari

import utils
from imports import *
from Bot.DataBase.badword import DBBadWord

bad_word_plugin = lightbulb.Plugin("server_managment.bad_word")


@bad_word_plugin.command()
@lightbulb.command("badword", "The Badword System")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
def bad_word(ctx):
    pass


@bad_word.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("word", "The word you want to add to the badword list", type=str, required=True)
@lightbulb.command("add", "Add a word to the badword list")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.Context):
    word = ctx.options.word.lower()

    if not DBBadWord(ctx.app.db).add_bad_word(ctx.guild_id, word):
        embed = hikari.Embed(
            title="❌ Error",
            description="The word is already in the badword list",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
    else:
        embed = hikari.Embed(title="✅ Success",
                             description=f"The word `{word}` has been added to the badword list",
                             color=utils.Color.green().__str__(),
                             timestamp=utils.get_time()
                             )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)


@bad_word.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("word", "The word you want to remove from the badword list", type=str, required=True)
@lightbulb.command("remove", "Remove a word from the badword list")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def remove(ctx: lightbulb.Context):
    word = ctx.options.word

    if not DBBadWord(ctx.app.db).remove_bad_word(ctx.guild_id, word):
        embed = hikari.Embed(
            title="❌ Error",
            description="The word is not in the badword list",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
    else:
        embed = hikari.Embed(
            title="✅ Success",
            description=f"The word `{word}` has been removed from the badword list",
            color=utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)


@bad_word.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("list", "List all the badwords")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def list(ctx: lightbulb.Context):
    bad_words = DBBadWord(ctx.app.db).get_bad_words(ctx.guild_id)
    if bad_words:
        bad_wordss = []
        for i in bad_words:
            if type(i)==str:
                bad_wordss.append(i)
            else:
                string='Badword Group: '
                for j in i:
                    string+=j+', '
                bad_wordss.append(string)

        embed = hikari.Embed(
            title="Badwords",
            description="\n".join([str(b) for b in bad_wordss]),
            color=utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
    else:
        embed = hikari.Embed(
            title="Badwords",
            description="There are no badwords in the list",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)


@bad_word.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.command("clear", "Clear the badword list")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def clear(ctx: lightbulb.Context):
    DBBadWord(ctx.app.db).clear_bad_words(ctx.guild_id)
    embed = hikari.Embed(
        title="✅ Success",
        description="The badword list has been cleared",
        color=utils.Color.green().__str__(),
        timestamp=utils.get_time()
    )
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=5)


@bad_word.child()
@lightbulb.check_exempt(utils.mod_check)
@lightbulb.option("words", "The words you want to add to the badword list. Separate words with a comma", type=str,
                  required=True)
@lightbulb.command("add-group", "Add multiple words to the badword list")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def add_many(ctx: lightbulb.Context):
    words = ctx.options.words.replace(" ", "").split(",")
    words = [word.lower() for word in words]
    if DBBadWord(ctx.app.db).add_bad_word(ctx.guild_id, words):
        embed = hikari.Embed(
            title="✅ Success",
            description="The word-group has been added to the badword list",
            color=utils.Color.green().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)
    else:
        embed = hikari.Embed(
            title="❌ Error",
            description="The word-group is already in the badword list",
            color=utils.Color.red().__str__(),
            timestamp=utils.get_time()
        )
        if ctx.interaction:
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond(embed=embed, delete_after=5)




@bad_word_plugin.listener(hikari.events.GuildMessageCreateEvent)
async def on_message(event: hikari.events.GuildMessageCreateEvent):
    if event.guild_id is None: return

    if not event.message.content: return

    if not DBBadWord(event.app.db).get_onoroff(event.guild_id): return

    bad_words = DBBadWord(event.app.db).get_bad_words(event.guild_id)

    if not bad_words: return
    for i in bad_words:
        if type(i) is str:
            if i.lower() in event.message.content.lower():
                await event.message.delete()
                return
        else:
            x=0
            for word in i:
                if word.lower() in event.message.content.lower(): x+=1
                if x == len(i):
                    await event.message.delete()
                    return

@bad_word.child()
@lightbulb.command("help", "Show the help for the badword system")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def help(ctx: lightbulb.Context):
    embed = hikari.Embed(
        title="Badword Help",
        description="This is the help for the badword system.\n"
                    "The badword system is used to prevent people from using bad words in the server.\n"
                    "The badword system is off by default.\n"
                    "To turn it on or off, use `/badword toggle <on/off>`\n"
                    "To see the badword list, use `/badword list`\n"
                    "To add a badword to the list, use `/badword add <word>`\n"
                    "To remove a badword from the list, use `/badword remove <word>`\n"
                    "To clear the badword list, use `/badword clear`\n"
                    "To add a word group to the badword list, use `/badword add-group <words>`\n"
                    "To see this help, use `/badword help`",
        color=utils.Color.blue().__str__(),
        timestamp=utils.get_time()
    )
    embed.add_field("Badword Groups", "You can add a group of words to the badword list.\n"
                    "A Badword Group is a list of words, and only when all of the words are used in a message, "
                    "the message will be deleted.\n")
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=5)


@bad_word.child()
@lightbulb.option("on_or_off", "Whether you want to turn the badword system on or off", type=str, required=True,choices=["on","off"])
@lightbulb.command("toggle", "Toggle the badword system on or off")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def toggle(ctx: lightbulb.Context):
    onoroff = ctx.options.on_or_off.lower()

    if onoroff == "on":
        DBBadWord(ctx.app.db).set_onoroff(ctx.guild_id, True)
    else:
        DBBadWord(ctx.app.db).set_onoroff(ctx.guild_id, False)

    embed = hikari.Embed(
        title="✅ Success",
        description="The badword system has been turned {}".format(onoroff),
        color=utils.Color.green().__str__(),
        timestamp=utils.get_time()
    )
    if ctx.interaction:
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(embed=embed, delete_after=5)


def load(bot):
    bot.add_plugin(bad_word_plugin)


def unload(bot):
    bot.remove_plugin(bad_word_plugin)
