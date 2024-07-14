import typing
import discord
from ..utils.online_resources import get_random_gif


def check_missing_files(attachments: typing.List[discord.Attachment], required_files: typing.List[str]) -> typing.List[str]:
    """Check for missing required files in the attachments."""
    missing_files = [file for file in required_files if not any(attachment.filename == file for attachment in attachments)]
    return missing_files


def generate_response_message(missing_files: typing.List[str], troubleshooting_channel_mention: str) -> str:
    """Generate the response message based on missing files."""
    random_gif = get_random_gif()
    if missing_files:
        missing_files_str = ", ".join(missing_files)
        return (f"Please attach the following missing files: {missing_files_str}. It's literally in the "
                f"{troubleshooting_channel_mention} channel which you should be reading.\n{random_gif}")
    elif missing_files is None:
        return f"Please upload the required log files (Olympus_log.txt and dcs.log).\n{random_gif}"
    else:
        return (f"Thank you for attaching the logs! Someone from the DCS Olympus Team will assist you eventually. "
                f"In the meantime, please check the {troubleshooting_channel_mention} channel, make sure you have "
                f"followed the instructions there.")

# TODO dcs.log check if the Olympus loading lines appear, In Olympus log file check for successful binding to the port
# TODO log_checker function
