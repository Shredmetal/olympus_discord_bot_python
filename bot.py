import discord
from discord.ext import commands, tasks
import os
from online_resources import get_random_gif
from helper_functions import check_missing_files, generate_response_message
from enum import Enum, auto

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

TROUBLESHOOTING_CHANNEL_ID = 1185842396873900032
ALLOWED_CHANNEL_ID = 1180168498413052015


class ThreadState(Enum):
    AWAITING_LOGS = auto()
    LOGS_RECEIVED = auto()


thread_states = {}


@bot.tree.command(name="support", description="Initiate an Olympus support request")
@commands.cooldown(1, 3600, commands.BucketType.user)
async def support(interaction: discord.Interaction):

    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        correct_channel = interaction.guild.get_channel(ALLOWED_CHANNEL_ID)
        if correct_channel:
            await interaction.response.send_message(
                f"This command can only be used in the designated support channel. "
                f"Please use {correct_channel.mention} for support requests.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "This command can only be used in the designated support channel. "
                "Please contact an administrator if you cannot find the support channel.",
                ephemeral=True
            )
        return

    troubleshooting_channel_mention = f"<#{TROUBLESHOOTING_CHANNEL_ID}>"

    thread_name = f"Support for {interaction.user.name}"
    try:
        thread = await interaction.channel.create_thread(name=thread_name, auto_archive_duration=1440)
    except discord.HTTPException:
        await interaction.response.send_message(content="Failed to create support thread. Please try again later.",
                                                ephemeral=True)
        return

    await interaction.response.send_message(
        content=f"Support thread created: {thread.mention}\nPlease upload your log files (Olympus_log.txt and dcs.log) "
                f"in this thread.",
        ephemeral=True
    )

    await thread.send(
        f"{interaction.user.mention} Welcome to your support thread. Before proceeding, please ensure you have read "
        f"all the information in the {troubleshooting_channel_mention} channel.\n\n"
        f"Once you've done that, please upload your Olympus_log.txt and dcs.log files here. After uploading, someone "
        f"from the DCS Olympus team will eventually get to you."
    )

    thread_states[thread.id] = ThreadState.AWAITING_LOGS

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.Thread) and message.channel.name.startswith("Support for"):
        thread_id = message.channel.id

        if message.author == bot.user:
            return

        if thread_states.get(thread_id) == ThreadState.AWAITING_LOGS:
            if message.attachments:
                attachments = message.attachments
                required_files = ["Olympus_log.txt", "dcs.log"]
                missing_files = check_missing_files(attachments, required_files)
                response_message = generate_response_message(missing_files,
                                                             f"<#{TROUBLESHOOTING_CHANNEL_ID}>")

                await message.channel.send(response_message)

                if not missing_files:
                    thread_states[thread_id] = ThreadState.LOGS_RECEIVED
            else:
                await request_logs(message.channel)

    await bot.process_commands(message)

async def request_logs(channel):
    random_gif = get_random_gif()
    reminder_message = "Please upload the required log files (Olympus_log.txt and dcs.log).\n" + random_gif
    await channel.send(reminder_message)

@tasks.loop(hours=72)
async def cleanup_old_threads():
    for guild in bot.guilds:
        for thread in guild.threads:
            if thread.name.startswith("Support for") and (discord.utils.utcnow() - thread.created_at).days > 7:
                try:
                    await thread.delete()
                    thread_states.pop(thread.id, None)
                except discord.HTTPException:
                    pass

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    cleanup_old_threads.start()

@support.error
async def support_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.CommandOnCooldown):
        await interaction.response.send_message(
            f"You can only use this command once per hour. Please try again in {error.retry_after:.2f} seconds.",
            ephemeral=True)
    else:
        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)

bot.run(os.environ['DISCORD_BOT_TOKEN'])
