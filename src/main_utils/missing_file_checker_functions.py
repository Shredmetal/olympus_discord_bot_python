import typing
import discord

from .enums import ThreadState
from ..main_utils.online_resources import get_random_gif


def check_missing_files(attachments: typing.List[discord.Attachment], required_files: typing.List[str]) -> typing.List[str]:
    """Check for missing required files in the attachments."""
    missing_files = [file for file in required_files if not any(attachment.filename == file for attachment in attachments)]
    return missing_files


def generate_response_message(missing_files: typing.Optional[typing.List[str]],
                              troubleshooting_channel_mention: str,
                              thread_state: ThreadState) -> str:
    """Generate the response message based on missing files."""
    random_gif = get_random_gif()
    if missing_files:
        missing_files_str = ", ".join(missing_files)
        return (f"Please attach the following missing files: {missing_files_str}. Please attach them to a single "
                f"message.\n"
                f"{random_gif}")
    elif missing_files is None:
        if thread_state == ThreadState.AWAITING_LOGS:
            return (f"Please upload the required log files (Olympus_log.txt and dcs.log) in a single message."
                    f"\n{random_gif}")
        elif thread_state == ThreadState.NO_OLYMPUS_LOGS:
            return f"Please upload the required log files (dcs.log) \n{random_gif}"
    else:
        return (f"Thank you for attaching the logs! We will get to you eventually, however, if you are experiencing "
                f"an issue listed on one of the buttons below, please click on them for faster resolution. "
                f"Also, make sure to check the {troubleshooting_channel_mention} channel, make sure you have "
                f"followed the instructions there.")
