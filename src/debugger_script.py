import re

# Updated regex patterns
successful_install_pattern = r'Olympus\.HOOKS\.LUA.*olympus\.dll loaded successfully|Olympus\.HOOKS\.LUA.*Olympus v.+? C\+\+ module callbacks registered correctly'
installation_process_pattern = r'Olympus\.HOOKS\.LUA.*Executing OlympusHook\.lua|Olympus\.HOOKS\.LUA.*Loading olympus\.dll from|Olympus\.dll.*Instance location retrieved successfully|Olympus\.dll.*Loading \.dlls from'

# Test content
content = """
2024-07-18 14:36:31.949 INFO    Olympus.HOOKS.LUA (Main): Executing OlympusHook.lua
2024-07-18 14:36:31.949 INFO    Olympus.HOOKS.LUA (Main): Loading olympus.dll from [C:\\Users\DCS\Saved Games\Borderzone1\Mods\Services\Olympus\\bin\]
2024-07-18 14:36:31.951 INFO    Olympus.dll (Main): Instance location retrieved successfully
2024-07-18 14:36:31.951 INFO    Olympus.dll (Main): Loading .dlls from C:\\Users\DCS\Saved Games\Borderzone1\Mods\Services\Olympus\\bin\\
2024-07-18 14:36:31.951 INFO    Olympus.HOOKS.LUA (Main): olympus.dll loaded successfully
2024-07-18 14:36:31.951 INFO    Olympus.HOOKS.LUA (Main): Olympus vyourmother C++ module callbacks registered correctly.
"""

# Run regex and print results
print("Successful installation matches:")
successful_install_matches = re.findall(successful_install_pattern, content, re.IGNORECASE | re.MULTILINE)
print(successful_install_matches)

print("\nInstallation process matches:")
installation_process_matches = re.findall(installation_process_pattern, content, re.IGNORECASE | re.MULTILINE)
print(installation_process_matches)