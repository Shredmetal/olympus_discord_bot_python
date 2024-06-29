from discord.ext import commands
import os
from .commands import register_commands
from .events import register_events
from ..utils.constants import INTENTS

bot = commands.Bot(command_prefix='/', intents=INTENTS)

register_commands(bot)
register_events(bot)

bot.run(os.environ['DISCORD_BOT_TOKEN'])
