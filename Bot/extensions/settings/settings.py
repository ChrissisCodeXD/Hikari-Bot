import lightbulb

from imports import *


settings_plugin = lightbulb.Plugin("settings.settings","all the Settings for the Bot")


async def generate_rows(bot,guild_id):
    pass






def load(bot):
    bot.add_plugin(settings_plugin)

def unload(bot):
    bot.remove_plugin(settings_plugin)