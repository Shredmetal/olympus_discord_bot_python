import typing
import discord


# Provided check_missing_files function
def check_missing_files(attachments: typing.List[discord.Attachment], required_files: typing.List[str]) -> typing.List[str]:
    """Check for missing required files in the attachments."""
    missing_files = [file for file in required_files if not any(attachment.filename == file for attachment in attachments)]
    return missing_files


def generate_response_message(missing_files: typing.List[str], troubleshooting_channel_mention: str) -> str:
    """Generate the response message based on missing files."""
    if missing_files:
        missing_files_str = ", ".join(missing_files)
        return (f"Please attach the following missing files: {missing_files_str}. It's literally in the "
                f"{troubleshooting_channel_mention} channel which you should be reading.")
    else:
        return (f"Thank you for attaching the logs! Someone from the DCS Olympus Team will assist you eventually. "
                f"In the meantime, please check the {troubleshooting_channel_mention} channel and read everything "
                f"there to ensure you have followed the instructions.")
