import discord

from .events_utils.events_utils import handle_awaiting_logs, handle_no_olympus_logs
from src.bot.events_utils.missing_file_checker_functions import generate_response_message
from ..main_utils.constants import TROUBLESHOOTING_CHANNEL_ID
from ..main_utils.enums import ThreadState
from src.main_utils.shared_state import get_thread_state, set_thread_state
from ..core.tasks import cleanup_old_threads


def register_events(bot):
    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Failed to sync commands: {e}")
        cleanup_old_threads.start(bot)

    @bot.event
    async def on_message(message):
        if isinstance(message.channel, discord.Thread):
            if message.channel.name.startswith("Support for"):
                thread_id = message.channel.id

                if message.author == bot.user:
                    return

                current_state = get_thread_state(thread_id)

                if current_state == ThreadState.AWAITING_LOGS:
                    await handle_awaiting_logs(message, thread_id, current_state, bot)
                elif current_state == ThreadState.NO_OLYMPUS_LOGS:
                    await handle_no_olympus_logs(message, thread_id, current_state, bot)
                elif current_state == ThreadState.LOGS_RECEIVED:
                    return
                elif current_state == ThreadState.CLOSED:
                    return
                else:
                    set_thread_state(thread_id, ThreadState.AWAITING_LOGS)
                    response_message = generate_response_message(None, f"<#{TROUBLESHOOTING_CHANNEL_ID}>")
                    await message.channel.send(response_message)

        await bot.process_commands(message)
