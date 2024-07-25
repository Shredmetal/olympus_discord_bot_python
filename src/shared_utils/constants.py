import os
import discord

INTENTS = discord.Intents.default()
INTENTS.message_content = True

TROUBLESHOOTING_CHANNEL_ID = int(os.getenv('TROUBLESHOOTING_CHANNEL_ID', '1185842396873900032'))
COMMUNITY_SUPPORT_CHANNEL_ID = int(os.getenv('COMMUNITY_SUPPORT_CHANNEL_ID', '1180168498413052015'))
SUPPORT_REQUESTS_ID = int(os.getenv('SUPPORT_REQUESTS_ID', '1265325469218246656'))


THREAD_CLOSED_STRING = ("This thread is no longer being monitored by the Olympus Discord Bot. Depending on your "
                        "interactions above, this means you either need to follow the instructions and install "
                        "/ reinstall DCS (Olympus), or a member of the DCS Olympus Team is looking into your "
                        "issue. Please be patient, as all of us have day jobs that need doing, which is how "
                        "DCS Olympus is kept completely free for you.")
