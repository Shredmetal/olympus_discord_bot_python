import re
from typing import List, Dict

from discord import Attachment


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


def process_dcs_log(content: str) -> List[str]:
    olympus_mentions = re.findall(r'(?i).*olympus.*', content)
    results = []
    # TODO: Apply processing logic to olympus_mentions and populate results
    return results


def process_olympus_log(content: str) -> List[str]:
    denied_mentions = re.findall(r'(?i).*denied.*', content)
    results = []
    # TODO: Apply processing logic to denied_mentions and populate results
    return results


async def process_attachments(attachments: List[Attachment]) -> Dict[str, List[str]]:
    log_contents = await download_attachments(attachments)
    results = {}

    if "dcs.log" in log_contents:
        results["dcs.log"] = process_dcs_log(log_contents["dcs.log"])

    if "Olympus_log.txt" in log_contents:
        results["Olympus_log.txt"] = process_olympus_log(log_contents["Olympus_log.txt"])

    return results


