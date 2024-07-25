from src.buttons.base_view import create_base_view
from src.buttons.problem_resolution_view import ResolutionView
from src.main_utils.shared_state import set_thread_state
from src.log_parsing.log_processor import process_attachments
from src.main_utils.constants import TROUBLESHOOTING_CHANNEL_ID, SUPPORT_REQUESTS_ID
from src.main_utils.enums import ThreadState
from src.main_utils.missing_file_checker_functions import generate_response_message, check_missing_files


async def handle_awaiting_logs(message, thread_id, current_state, bot):
    if not message.attachments:
        response_message = generate_response_message(None, f"<#{TROUBLESHOOTING_CHANNEL_ID}>", current_state)
        await message.channel.send(response_message)
        return

    attachments = message.attachments
    required_files = ["Olympus_log.txt", "dcs.log"]
    missing_files = check_missing_files(attachments, required_files)
    response_message = generate_response_message(
        missing_files=missing_files,
        troubleshooting_channel_mention=f"<#{TROUBLESHOOTING_CHANNEL_ID}>",
        thread_state=current_state
    )

    if missing_files:
        await message.channel.send(response_message)
        return

    set_thread_state(thread_id, ThreadState.LOGS_RECEIVED)
    await message.channel.send(response_message, view=create_base_view("common_issues"))

    analysis_results = await process_attachments(attachments)

    for log_file, results in analysis_results.items():
        if log_file == "Olympus_log.txt":
            if results:
                for result in results:
                    await message.channel.send(
                        result,
                        view=ResolutionView(include_not_resolved_no_logs=False)
                    )
            else:
                await message.channel.send(f"No issues found in {log_file}")

        # TODO Implement the dcs.log parsing logic
        # elif log_file == "dcs.log":
        #     if results:
        #         await message.channel.send(f"Issues found in {log_file}:")
        #         for issue in results:
        #             await message.channel.send(issue)
        #     else:
        #         await message.channel.send(f"No issues found in {log_file}")

    await notify_support_requests(bot, message.channel, message.author)


async def handle_no_olympus_logs(message, thread_id, current_state, bot):
    if not message.attachments:
        response_message = generate_response_message(None, f"<#{TROUBLESHOOTING_CHANNEL_ID}>", current_state)
        await message.channel.send(response_message)
        return

    attachments = message.attachments
    required_dcs_log = ["dcs.log"]
    missing_dcs_log = check_missing_files(attachments, required_dcs_log)
    no_olympus_log_response_message = generate_response_message(
        missing_files=missing_dcs_log,
        troubleshooting_channel_mention=f"<#{TROUBLESHOOTING_CHANNEL_ID}>",
        thread_state=current_state
    )

    if not missing_dcs_log:
        set_thread_state(thread_id, ThreadState.DCS_LOG_RECEIVED)
        await message.channel.send(no_olympus_log_response_message, view=create_base_view("common_issues"))

        # analysis_results = await process_attachments(attachments)

        # for log_file, results in analysis_results.items():
        #     TODO Implement the dcs.log parsing logic
        #     if log_file == "dcs.log":
        #         if results:
        #             await message.channel.send(f"Issues found in {log_file}:")
        #             for issue in results:
        #                 await message.channel.send(issue)
        #         else:
        #             await message.channel.send(f"No issues found in {log_file}")

        await notify_support_requests(bot, message.channel, message.author)
    else:
        await message.channel.send(no_olympus_log_response_message)


async def notify_support_requests(bot, thread, user):
    pantheon_channel = bot.get_channel(SUPPORT_REQUESTS_ID)
    if pantheon_channel:
        user_identifier = f"{user.name}#{user.discriminator}"
        await pantheon_channel.send(
            f"Support request received with logs at {thread.mention} from user: {user_identifier}")
    else:
        print(f"OLYMPUS DEBUG: Could not find the Pantheon channel with ID {SUPPORT_REQUESTS_ID}")
