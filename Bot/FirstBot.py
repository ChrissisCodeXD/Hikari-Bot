import hikari

from imports import *

_BotT = t.TypeVar("_BotT", bound="Bot")

from Bot import __version__, __prefix__, __beta__, __guilds__

log = logging.getLogger(__name__)


class FirstBot(lightbulb.BotApp):
    def __init__(self):
        self._extensions = [p.stem for p in Path("./extensions/").glob("*.py")]
        self._extensions.extend([f"moderation.{p.stem}" for p in Path("./extensions/moderation/").glob("*.py")])
        self.env = env()
        self.token = token = self.env.get('TOKEN1')
        if __beta__ == True:

            super().__init__(
                token=token,
                intents=hikari.Intents.ALL,
                prefix=lightbulb.app.when_mentioned_or(__prefix__),
                default_enabled_guilds=__guilds__
            )
        else:
            super().__init__(
                token=token,
                intents=hikari.Intents.ALL,
                prefix=lightbulb.app.when_mentioned_or(__prefix__),
                ignore_bots=True,
                case_insensitive_prefix_commands=True,
                logs={
                    "version": 1,
                    "incremental": True,
                    "loggers": {
                        "hikari": {"level": "INFO"},
                        "lightbulb": {"level": "INFO"},
                    },
                },
            )

    def run(self: _BotT) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.VoiceStateUpdateEvent, self.on_voice_state_update)
        self.event_manager.subscribe(hikari.VoiceServerUpdateEvent, self.on_voice_server_update)

        super().run(
            activity=hikari.Activity(
                name=f"Version {__version__}",
                type=hikari.ActivityType.COMPETING,
            )
        )

    async def on_starting(self: _BotT, event: hikari.StartingEvent) -> None:
        for ext in self._extensions:
            self.load_extensions(f"Bot.extensions.{ext}")
            log.info(f"'{ext}' extension loaded")

        # cache = sake.redis.RedisCache(self, self, address="redis://127.0.0.1")
        # await cache.open()
        # log.info("Connected to Redis server")

    async def on_started(self: _BotT, event: hikari.StartedEvent) -> None:
        """builder = (
            lavasnek_rs.LavalinkBuilder(int(b64decode(self.token.split(".")[0])), self.token)
            .set_host("127.0.0.1")
        )

        builder.set_start_gateway(False)
        self.lavalink = await builder.build(EventHandler())
        log.info("Created Lavalink instance")

        # self.stdout_channel = await self.rest.fetch_channel(STDOUT_CHANNEL_ID)
        # await self.stdout_channel.send(f"Testing v{__version__} now online!")"""
        log.info("Bot ready")

    async def on_stopping(self: _BotT, event: hikari.StoppingEvent) -> None:
        # This is gonna be fixed.
        # await self.stdout_channel.send(f"Testing v{__version__} is shutting down.")
        ...

    async def on_voice_state_update(self, event: hikari.VoiceStateUpdateEvent) -> None:
        print(f"event || on_voice_state_update || triggerd")

    async def on_voice_server_update(self, event: hikari.VoiceServerUpdateEvent) -> None:
        print(f"event || on_voice_server_update || triggerd")

    async def error_handler(self, event: lightbulb.CommandErrorEvent):
        print("event error")
