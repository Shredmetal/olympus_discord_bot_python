
from discord.ext import commands
import os
from .commands import register_commands
from .events import register_events
from ..utils.constants import INTENTS
from ..utils.views import LogOptionsView, ResolutionView

bot = commands.Bot(command_prefix='/', intents=INTENTS)

register_commands(bot)
register_events(bot)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    bot.add_view(LogOptionsView())
    bot.add_view(ResolutionView())

bot.run(os.environ['DISCORD_BOT_TOKEN'])
