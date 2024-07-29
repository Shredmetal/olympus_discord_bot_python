import re
from typing import List

from src.shared_utils.constants import COMMUNITY_SUPPORT_CHANNEL_ID


def process_dcs_log(content: str) -> List[str]:
    successful_install_pattern = (r'Olympus\.HOOKS\.LUA.*olympus\.dll loaded successfully|Olympus\.HOOKS\.LUA.*Olympus '
                                  r'v.+? C\+\+ module callbacks registered correctly')
    installation_process_pattern = (r'Olympus\.HOOKS\.LUA.*Executing OlympusHook\.lua|Olympus\.HOOKS\.LUA.*Loading '
                                    r'olympus\.dll from|Olympus\.dll.*Instance location retrieved successfully|Olympus\
                                    .dll.*Loading \.dlls from')

    successful_install_matches = re.findall(successful_install_pattern, content, re.IGNORECASE | re.MULTILINE)
    execution_process_matches = re.findall(installation_process_pattern, content, re.IGNORECASE | re.MULTILINE)

    no_install_match_string = "ISSUE: Lines indicating successful Olympus Installation not found!"
    no_execution_match_string = "ISSUE: Lines indicating Olympus process execution not found!"

    install_status = successful_install_matches if successful_install_matches else [no_install_match_string]
    execution_status = execution_process_matches if execution_process_matches else [no_execution_match_string]

    results = [f"Your dcs.log file analysis:\n\n"
               f"Olympus Installation: {install_status}\n\n"
               f"Olympus Process Execution: {execution_status}\n\n"
               f"Remarks:"]

    if successful_install_matches and execution_process_matches:
        results.append(f"Olympus appears to be correctly installed and running for the instance of DCS to which this "
                       f"dcs.log pertains. If you are still experiencing problems, please look through the common "
                       f"issues list button and if nothing there solves your issue, indicate so "
                       f"using the subsequently provided buttons and a member of the DCS Olympus Team will get "
                       f"around to helping you.")
    elif successful_install_matches and not execution_process_matches:
        results.append(f"This means that DCS Olympus has probably been correctly installed for the DCS instance to "
                       f"which this dcs.log pertains. However, the Olympus processes seem to have an issue running. "
                       f"Please click the common issues list button and attempt further troubleshooting from there. If "
                       f"that fails, just indicate that your issue is not resolved and a member of the DCS Olympus "
                       f"Team will get around to helping you out.")
    elif not successful_install_matches and execution_process_matches:
        results.append(f"Have an award. We're not quite sure how you managed it but your log seems to indicate that "
                       f"Olympus has not been installed for this DCS instance but somehow certain Olympus processes "
                       f"appear to be running. Either way, please click the common issues list button and try to "
                       f"troubleshoot from there. If you are not able to, make the appropriate selection and one of us "
                       f"will get to you.")
    else:
        results.append(f"Olympus does not appear to be installed or running for this instance of DCS. Please ensure "
                       f"that Olympus is installed correctly and try again. You may also find it useful to look "
                       f"through the common issues list using the provided button. If you experience further issues "
                       f"after ensuring that DCS Olympus has been correctly installed, please use the /support "
                       f"command in <#{COMMUNITY_SUPPORT_CHANNEL_ID}> again.")

    return results
