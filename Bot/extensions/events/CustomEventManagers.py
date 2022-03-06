from imports import *
from utils import EveryoneMentionedEvent, BotMentionedEvent

event_plugin = lightbulb.Plugin("event_plugin")


@event_plugin.listener(hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent):
    if not event.content: return
    if "@everyone" in event.content or "@here" in event.content:
        event = EveryoneMentionedEvent(
            author=event.author,
            content=event.content,
            message_id=event.message_id,
            channel_id=event.channel_id,
            type="everyone" if "@everyone" in event.content else "here",
            original_event=event
        )

        event_plugin.bot.dispatch(event)
    if f"<@{event.app.application.id}>" in event.content:
        event = BotMentionedEvent(
            author=event.author,
            content=event.content,
            message_id=event.message_id,
            channel_id=event.channel_id,
            original_event=event
        )

        event_plugin.bot.dispatch(event)




def load(bot):
    bot.add_plugin(event_plugin)


def unload(bot):
    bot.remove_plugin(event_plugin)
