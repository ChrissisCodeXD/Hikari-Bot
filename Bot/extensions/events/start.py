from imports import *

log = logging.getLogger(__name__)

start_plugin = lightbulb.Plugin("start_event_plugin")


@start_plugin.listener(lightbulb.LightbulbStartedEvent)
async def on_start(event: lightbulb.LightbulbStartedEvent):
    print("Bot ready")
    print(
        f"Invite URL: https://discord.com/api/oauth2/authorize?client_id={event.app.application.id}&permissions=8&scope=bot%20applications.commands")


def load(bot):
    bot.add_plugin(start_plugin)


def unload(bot):
    bot.remove_plugin(start_plugin)
