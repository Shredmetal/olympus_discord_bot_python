import re
from typing import List, Dict, Union

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


def process_olympus_log(content: str) -> str:
    access_denied_mentions = re.findall(r"Access denied: attempting to add Address", content)
    if not access_denied_mentions:
        return ""
    else:
        return ("Access denied detected in Olympus_log.txt - likely causes of this are: \n\n(1) You did not use netsh "
                "to remove a URL reservation or \n\n(2) you picked to enable direct backend connections but did NOT do "
                "a URL reservation to allow it to bind the port. \n\nThis was specified in the installation "
                "instructions. Either way, in DCS Olympus v1.0.4, we have removed the need to use the netsh spell in "
                "your command line spellcasting interface, however, you will need to remove it if you have done so "
                "previously. Please follow the instructions "
                "[here](https://github.com/Pax1601/DCSOlympus/wiki#123-removing-the-net-shell-netsh-rule). "
                "\n\n(It's not really a spell, it's a command to a computer, because spells are magic and magic is "
                "heresy)")


async def process_attachments(attachments: List[Attachment]) -> Dict[str, Union[List[str], str]]:
    log_contents = await download_attachments(attachments)
    results = {}

    if "dcs.log" in log_contents:
        results["dcs.log"] = process_dcs_log(log_contents["dcs.log"])

    if "Olympus_log.txt" in log_contents:
        results["Olympus_log.txt"] = process_olympus_log(log_contents["Olympus_log.txt"])

    return results


