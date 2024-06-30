from discord import Permissions

perms = Permissions(1829903095950400)

print(f"Create Public Threads: {perms.create_public_threads}")
print(f"Send Messages: {perms.send_messages}")
print(f"Read Messages: {perms.read_messages}")
print(f"Manage Channels: {perms.manage_channels}")
print(f"Manage Threads: {perms.manage_threads}")