from bot import FirstBot
import os
import requests
from lightbulb.ext import tasks

if os.name != "nt":
    # import uvloop
    pass
    # uvloop.install()

if __name__ == "__main__":
    bot = FirstBot()
    tasks.load(bot)
    bot.run()
