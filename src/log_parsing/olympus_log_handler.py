
import re
from typing import List


def process_olympus_log(content: str) -> List[str]:
    responses = []
    access_denied_mentions = re.findall(r"Access denied: attempting to add Address", content, re.MULTILINE)
    port_in_use_mentions = re.findall(r"Address\s+'([^']+)'\s+is already in use", content, re.MULTILINE)

    if access_denied_mentions:
        responses.append("Your Olympus_log.txt file analysis:\n\n"
                         "Access denied detected in Olympus_log.txt - likely causes of this are: \n\n\t(1) You did not "
                         "use netsh to remove a URL reservation or \n\n\t(2) you picked to enable direct backend "
                         "connections but did NOT do a URL reservation to allow it to bind the port. \n\nThis was "
                         "specified in the installation instructions. Either way, in DCS Olympus v1.0.4, we have "
                         "removed the need to use the netsh spell in your command line spellcasting interface, "
                         "however, you will need to remove it if you have done so previously. Please follow the "
                         "instructions "
                         "[here](https://github.com/Pax1601/DCSOlympus/wiki#123-removing-the-net-shell-netsh-rule). "
                         "\n\n(It's not really a spell, it's a command to a computer, because spells are magic and "
                         "magic is heresy)")

    if port_in_use_mentions:
        responses.append(f"The following addresses were found to be in use in Olympus_log.txt - \n\n"
                         f"{port_in_use_mentions}.\n\n Please use Olympus Manager to change the port in use by the "
                         f"Olympus Server. There are some instructions "
                         f"[here](https://github.com/Pax1601/DCSOlympus/wiki#245-set-port-and-address-settings).")

    return responses
