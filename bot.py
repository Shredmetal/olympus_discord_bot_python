import discord
from discord.ext import commands
import os
import typing
from online_resources import get_random_gif
from helper_functions import check_missing_files, generate_response_message
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# ID of the troubleshooting channel
TROUBLESHOOTING_CHANNEL_ID = 1185842396873900032


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')



@bot.command(name='support')
async def support(ctx):
    troubleshooting_channel_mention = f"<#{TROUBLESHOOTING_CHANNEL_ID}>"
    required_files = ["Olympus_log.txt", "dcs.log"]

    # Correctly access attachments from ctx.message.attachments
    attachments = ctx.message.attachments

    if attachments:
        # Use the provided check_missing_files function
        missing_files = check_missing_files(attachments, required_files)
        response_message = generate_response_message(missing_files, troubleshooting_channel_mention)
        await ctx.send(response_message)
    else:
        await ctx.send(f"Please attach logs. It's literally in the {troubleshooting_channel_mention} channel which you should be reading.")
        random_gif = get_random_gif()
        await ctx.send(random_gif)

bot.run(os.getenv('DISCORD_TOKEN'))
