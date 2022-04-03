import logging
import typing as t
from pathlib import Path
from logger.main_loggers import Logger

__guilds__ = (948904191559077888,764397934476263464)

__testing__ = True
__beta__ = True
__prefix__ = "!"
__productname__ = "1. Test Bot"
__version__ = "0.0.2.3beta"
__description__ = "A Discord bot designed for the Carberra Tutorials Discord server."
__url__ = "https://github.com/ChrissisCodeXD/Hikari-TestProject"
__authors__ = ("Christopher Mehnert")
__license__ = "BSD-3-Clause"
__bugtracker__ = "https://github.com/ChrissisCodeXD/Hikari-TestProject/issues"
__ci__ = "https://github.com/ChrissisCodeXD/Hikari-TestProject/actions/new"

ROOT_DIR: t.Final = Path(__file__).parent

logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)
logging.getLogger("py.warnings").setLevel(logging.ERROR)
