import discord
from ..utils.helper_functions import check_missing_files, generate_response_message
from ..utils.online_resources import get_random_gif
from ..utils.constants import TROUBLESHOOTING_CHANNEL_ID, PANTHEON_CHANNEL_ID
from ..utils.enums import ThreadState
from ..core.shared_state import get_thread_state, set_thread_state
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
        # Check if the message is in a thread
        if isinstance(message.channel, discord.Thread):
            # Check if it's a support thread
            if message.channel.name.startswith("Support for"):
                thread_id = message.channel.id

                # Ignore messages from the bot itself
                if message.author == bot.user:
                    return

                # Get the current thread state, default to AWAITING_LOGS if not set
                current_state = get_thread_state(thread_id)

                if current_state == ThreadState.AWAITING_LOGS:
                    if message.attachments:
                        attachments = message.attachments
                        required_files = ["Olympus_log.txt", "dcs.log"]
                        missing_files = check_missing_files(attachments, required_files)
                        response_message = generate_response_message(missing_files,
                                                                     f"<#{TROUBLESHOOTING_CHANNEL_ID}>")

                        await message.channel.send(response_message)

                        if not missing_files:
                            set_thread_state(thread_id, ThreadState.LOGS_RECEIVED)
                            await notify_pantheon(bot, message.channel, message.author)
                    else:
                        await request_logs(message.channel)
                elif current_state == ThreadState.LOGS_RECEIVED:
                    return
                else:
                    # If the thread state is not set or in an unexpected state, set it to AWAITING_LOGS
                    set_thread_state(thread_id, ThreadState.AWAITING_LOGS)
                    await request_logs(message.channel)

        # This line is important to process commands
        await bot.process_commands(message)


async def request_logs(channel):
    random_gif = get_random_gif()
    reminder_message = "Please upload the required log files (Olympus_log.txt and dcs.log).\n" + random_gif
    await channel.send(reminder_message)

async def notify_pantheon(bot, thread, user):
    pantheon_channel = bot.get_channel(PANTHEON_CHANNEL_ID)
    if pantheon_channel:
        user_identifier = f"{user.name}#{user.discriminator}"
        await pantheon_channel.send(
            f"Support request received with logs at {thread.mention} from user: {user_identifier}")
    else:
        print(f"OLYMPUS DEBUG: Could not find the Pantheon channel with ID {PANTHEON_CHANNEL_ID}")
