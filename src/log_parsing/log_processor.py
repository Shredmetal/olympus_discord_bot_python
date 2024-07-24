from typing import List, Dict

from discord import Attachment

from src.log_parsing.dcs_log_handler import process_dcs_log
from src.log_parsing.olympus_log_handler import process_olympus_log


async def download_attachments(attachments: List[Attachment]) -> Dict[str, str]:
    log_contents = {}
    for attachment in attachments:
        if attachment.filename in ["Olympus_log.txt", "dcs.log"]:
            try:
                content = await attachment.read()
                log_contents[attachment.filename] = content.decode('utf-8')
            except Exception as e:
                print(f"Error downloading {attachment.filename}: {str(e)}")
    return log_contents


async def process_attachments(attachments: List[Attachment]) -> Dict[str, List[str]]:
    log_contents = await download_attachments(attachments)
    results = {}

    if "dcs.log" in log_contents:
        results["dcs.log"] = process_dcs_log(log_contents["dcs.log"])

    if "Olympus_log.txt" in log_contents:
        results["Olympus_log.txt"] = process_olympus_log(log_contents["Olympus_log.txt"])

    return results
