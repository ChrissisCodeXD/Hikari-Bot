from imports import *
from Bot.logger.main_loggers import Logger
log = logging.getLogger(__name__)

Log = Logger()
start_plugin = lightbulb.Plugin("start_event_plugin")


@start_plugin.listener(lightbulb.LightbulbStartedEvent)
async def on_start(event: lightbulb.LightbulbStartedEvent):
    print("Bot ready")
    print(
        f"Invite URL: https://discord.com/api/oauth2/authorize?client_id={event.app.application.id}&permissions=8&scope=bot%20applications.commands")
    Log.send_on_start(event.app)

def load(bot):
    bot.add_plugin(start_plugin)


def unload(bot):
    bot.remove_plugin(start_plugin)
