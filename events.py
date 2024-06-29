import discord
from helper_functions import check_missing_files, generate_response_message
from online_resources import get_random_gif
from constants import TROUBLESHOOTING_CHANNEL_ID
from enums import ThreadState
from tasks import cleanup_old_threads

thread_states = {}


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
                current_state = thread_states.get(thread_id, ThreadState.AWAITING_LOGS)

                if current_state == ThreadState.AWAITING_LOGS:
                    if message.attachments:
                        attachments = message.attachments
                        required_files = ["Olympus_log.txt", "dcs.log"]
                        missing_files = check_missing_files(attachments, required_files)
                        response_message = generate_response_message(missing_files,
                                                                     f"<#{TROUBLESHOOTING_CHANNEL_ID}>")

                        await message.channel.send(response_message)

                        if not missing_files:
                            thread_states[thread_id] = ThreadState.LOGS_RECEIVED
                    else:
                        await request_logs(message.channel)
                elif current_state == ThreadState.LOGS_RECEIVED:
                    return
                else:
                    # If the thread state is not set or in an unexpected state, set it to AWAITING_LOGS
                    thread_states[thread_id] = ThreadState.AWAITING_LOGS
                    await request_logs(message.channel)

        # This line is important to process commands
        await bot.process_commands(message)


async def request_logs(channel):
    random_gif = get_random_gif()
    reminder_message = "Please upload the required log files (Olympus_log.txt and dcs.log).\n" + random_gif
    await channel.send(reminder_message)