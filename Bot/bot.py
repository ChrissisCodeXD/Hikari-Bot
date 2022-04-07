import hikari
import lightbulb

import utils
from imports import *

_BotT = t.TypeVar("_BotT", bound="Bot")

from Bot.DataBase.Connection import DBConnection
from Bot.DataBase.prefix import DBPrefix
from Bot.DataBase.warnsys import DBwarn
from Bot.DataBase.mutesys import DBMute
from Bot.DataBase.settings import DBSettings
from Bot.DataBase.erros import DBErros
from Bot.DataBase.welcome import *
from Bot.DataBase.cocsys import DBCoc
from Bot.DataBase.LinkSystem import DBLink
from Bot.DataBase.levelsys import DBLevel
from Bot.DataBase.auto_role import DBRole
from Bot.DataBase.badword import DBBadWord
from Bot.DataBase.logChannel import DBlog
from Bot.DataBase.aduitlogsys import DBAuditLog
from Bot import __version__, __prefix__, __beta__, __guilds__
from utils import HelpCommand

log = logging.getLogger(__name__)


class Prefixes:

    def __init__(self, bot):
        self.bot = bot
        self.prefixes = {}
        self.prefixes = DBPrefix(self.bot.db).get_all_prefixes()

    def get_prefix(self, guild_id):

        if str(guild_id) not in self.prefixes:
            result = DBPrefix(self.bot.db).get_all_prefixes()
            if str(guild_id) not in result:
                result[str(guild_id)] = "!"
                DBPrefix(self.bot.db).insert_one(guild_id, "!")
            self.prefixes = result
        return self.prefixes.get(str(guild_id))

    def get_prefixes(self, bot, msg):
        return self.get_prefix(msg.guild_id)

    def change_prefix(self, guild_id, prefix):
        result = DBPrefix(self.bot.db).get_prefix_for_guild(guild_id)
        if len(result) == 0:
            DBPrefix(self.bot.db).insert_one(guild_id, prefix)
        else:
            DBPrefix(self.bot.db).update_one(guild_id, prefix)
        result = DBPrefix(self.bot.db).get_all_prefixes()
        self.prefixes = result


class FirstBot(lightbulb.BotApp):
    def __init__(self):
        self.log = log
        self.db = DBConnection()
        self._prefix__get_class = Prefixes(self)
        self._extensions = [p.stem for p in Path("./extensions/").glob("*.py")]
        self._extensions.extend([f"moderation.{p.stem}" for p in Path("./extensions/moderation/").glob("*.py")])
        self._extensions.extend([f"events.{p.stem}" for p in Path("./extensions/events/").glob("*.py")])
        self._extensions.extend([f"settings.{p.stem}" for p in Path("./extensions/settings/").glob("*.py")])
        self._extensions.extend([f"test.{p.stem}" for p in Path("./extensions/test/").glob("*.py")])
        self._extensions.extend([f"security.{p.stem}" for p in Path("./extensions/security/").glob("*.py")])
        self._extensions.extend([f"fun.{p.stem}" for p in Path("./extensions/fun/").glob("*.py")])
        self._extensions.extend(
            [f"server_managment.{p.stem}" for p in Path("./extensions/server_managment/").glob("*.py")])
        self.env = utils.env()
        self.token = token = self.env.get('TOKEN1')
        if __beta__ == True:

            super().__init__(
                token=token,
                intents=hikari.Intents.ALL,
                prefix=lightbulb.app.when_mentioned_or(self._prefix__get_class.get_prefixes),
                default_enabled_guilds=__guilds__,
                help_class=HelpCommand,
                help_slash_command=True,
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
        else:
            super().__init__(
                token=token,
                intents=hikari.Intents.ALL,
                prefix=lightbulb.app.when_mentioned_or(self._prefix__get_class.get_prefixes),
                ignore_bots=True,
                help_class=HelpCommand,
                help_slash_command=True,
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
        DBPrefix(self.db).create()
        DBwarn(self.db).create()
        DBMute(self.db).create()
        DBSettings(self.db).create()
        DBErros(self.db).create()
        DBWelcomeChannel(self.db).create()
        DBCoc(self.db).create()
        DBLink(self.db).create()
        DBLevel(self.db).create()
        DBRole(self.db).create()
        DBBadWord(self.db).create()
        DBlog(self.db).create()
        DBAuditLog(self.db).create()

        # cache = sake.redis.RedisCache(self, self, address="redis://127.0.0.1")
        # await cache.open()
        # log.info("Connected to Redis server")

    async def on_started(self: _BotT, event: lightbulb.LightbulbStartedEvent) -> None:
        """builder = (
            lavasnek_rs.LavalinkBuilder(int(b64decode(self.token.split(".")[0])), self.token)
            .set_host("127.0.0.1")
        )

        builder.set_start_gateway(False)
        self.lavalink = await builder.build(EventHandler())
        log.info("Created Lavalink instance")

        # self.stdout_channel = await self.rest.fetch_channel(STDOUT_CHANNEL_ID)
        # await self.stdout_channel.send(f"Testing v{__version__} now online!")"""

    async def on_stopping(self: _BotT, event: hikari.StoppingEvent) -> None:
        # This is gonna be fixed.
        # await self.stdout_channel.send(f"Testing v{__version__} is shutting down.")
        ...

    async def on_voice_state_update(self, event: hikari.VoiceStateUpdateEvent) -> None:
        return

    async def on_voice_server_update(self, event: hikari.VoiceServerUpdateEvent) -> None:
        return
