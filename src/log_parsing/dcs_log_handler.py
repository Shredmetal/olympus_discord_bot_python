import re
from typing import List


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
    results = [f"Your dcs.log file analysis:\n\n"
               f"Olympus Installation: {successful_install_matches}\n\n"
               f"Olympus Process Execution: {execution_process_matches}\n\n"]

    if ((successful_install_matches != [no_install_match_string])
            and (execution_process_matches != [no_execution_match_string])):
        results.append(f"Olympus appears to be correctly installed and running for the instance of DCS to which this "
                       f"dcs.log pertains. If you are still experiencing problems, please look through the common "
                       f"issues list (button provided above) and if nothing there solves your issue, indicate so "
                       f"using the subsequently provided buttons and a member of the DCS Olympus Team will get "
                       f"around to helping you.")
    elif ((successful_install_matches != [no_install_match_string])
          and (execution_process_matches == [no_execution_match_string])):
        results.append(f"This means that DCS Olympus has probably been correctly installed for the DCS instance to "
                       f"which this dcs.log pertains. However, the Olympus processes seem to have an issue running. "
                       f"Please click the common issues button and attempt further troubleshooting from there. If that "
                       f"fails, just indicate that your issue is not resolved and a member of the DCS Olympus Team "
                       f"will get around to helping you out.")
    elif ((successful_install_matches == [no_install_match_string]) and
          (execution_process_matches != [no_execution_match_string])):
        results.append(f"Have an award. We're not quite sure how you managed it but your log seems to indicate that "
                       f"Olympus has not been installed for this DCS instance but somehow certain Olympus processes "
                       f"appear to be running. Either way, please click the common issues button and try to "
                       f"troubleshoot from there. If you are not able to, make the appropriate selection and one of us "
                       f"will get to you.")

    return results
