import discord

from ..buttons.logs_received_views import LogsReceivedView
from ..buttons.problem_resolution_view import ResolutionView
from ..log_parsing.log_processor import process_attachments
from ..utils.helper_functions import check_missing_files, generate_response_message
from ..utils.constants import TROUBLESHOOTING_CHANNEL_ID, SUPPORT_REQUESTS_ID
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
        if isinstance(message.channel, discord.Thread):
            if message.channel.name.startswith("Support for"):
                thread_id = message.channel.id

                if message.author == bot.user:
                    return

                current_state = get_thread_state(thread_id)

                if current_state == ThreadState.AWAITING_LOGS:
                    if message.attachments:
                        attachments = message.attachments
                        required_files = ["Olympus_log.txt", "dcs.log"]
                        missing_files = check_missing_files(attachments, required_files)
                        response_message = generate_response_message(missing_files,
                                                                     f"<#{TROUBLESHOOTING_CHANNEL_ID}>")

                        if not missing_files:

                            set_thread_state(thread_id, ThreadState.LOGS_RECEIVED)
                            await message.channel.send(response_message, view=LogsReceivedView())

                            analysis_results = await process_attachments(attachments)

                            for log_file, results in analysis_results.items():
                                if log_file == "Olympus_log.txt":
                                    if results:
                                        for result in results:
                                            await message.channel.send(result, view=ResolutionView())
                                    else:
                                        await message.channel.send(f"No issues found in {log_file}")

                                # TODO Implement the dcs.log parsing logic
                                # elif log_file == "dcs.log":
                                #     if result:
                                #         await message.channel.send(f"Issues found in {log_file}:")
                                #         for issue in result:
                                #             await message.channel.send(issue)
                                #     else:
                                #         await message.channel.send(f"No issues found in {log_file}")

                            await notify_pantheon(bot, message.channel, message.author)
                        else:
                            await message.channel.send(response_message)
                    else:
                        response_message = generate_response_message(None, f"<#{TROUBLESHOOTING_CHANNEL_ID}>")
                        await message.channel.send(response_message)
                elif current_state == ThreadState.LOGS_RECEIVED:
                    return
                elif current_state == ThreadState.CLOSED:
                    return
                else:
                    set_thread_state(thread_id, ThreadState.AWAITING_LOGS)
                    response_message = generate_response_message(None, f"<#{TROUBLESHOOTING_CHANNEL_ID}>")
                    await message.channel.send(response_message)

        await bot.process_commands(message)


async def notify_pantheon(bot, thread, user):
    pantheon_channel = bot.get_channel(SUPPORT_REQUESTS_ID)
    if pantheon_channel:
        user_identifier = f"{user.name}#{user.discriminator}"
        await pantheon_channel.send(
            f"Support request received with logs at {thread.mention} from user: {user_identifier}")
    else:
        print(f"OLYMPUS DEBUG: Could not find the Pantheon channel with ID {SUPPORT_REQUESTS_ID}")
