from discord.ext import commands
import os
from .commands import register_commands
from .events import register_events
from ..buttons.common_issues_buttons.common_issues_list_view import CommonIssuesListView
from ..buttons.common_issues_buttons.common_issues_view import CommonIssuesView
from ..buttons.logs_view import InitialView
from ..main_utils.constants import INTENTS
from ..buttons.problem_resolution_view import ResolutionView

bot = commands.Bot(command_prefix='/', intents=INTENTS)

register_commands(bot)
register_events(bot)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    bot.add_view(InitialView())
    bot.add_view(ResolutionView())
    bot.add_view(CommonIssuesListView())
    bot.add_view(CommonIssuesView())

bot.run(os.environ['DISCORD_BOT_TOKEN'])
