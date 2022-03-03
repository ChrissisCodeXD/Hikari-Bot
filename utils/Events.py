import attr
import hikari

from hikari.traits import RESTAware
from hikari.events.base_events import Event
from hikari.users import User
from hikari.snowflakes import Snowflake

@attr.define()
class EveryoneMentionedEvent(Event):
    app: RESTAware = attr.field()

    author: User = attr.field()
    '''The user who mentioned everyone.'''

    content: str = attr.field()
    '''The message that was sent.'''

    message_id: Snowflake = attr.field()
    '''The message ID.'''

    channel_id: Snowflake = attr.field()
    '''The channel ID.'''

    type: str = attr.field()
    '''The Type of the Mention: here or everyone'''

    original_event: hikari.MessageCreateEvent = attr.field()
    '''The Original Data of the Message Event'''


@attr.define()
class BotMentionedEvent(Event):
    app: RESTAware = attr.field()

    author: User = attr.field()
    '''The user who mentioned everyone.'''

    content: str = attr.field()
    '''The message that was sent.'''

    message_id: Snowflake = attr.field()
    '''The message ID.'''

    channel_id: Snowflake = attr.field()
    '''The channel ID.'''

    original_event: hikari.MessageCreateEvent = attr.field()
    '''The Original Data of the Message Event'''