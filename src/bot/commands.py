import discord
from discord import app_commands
from discord.ext import commands

from .commands_utils.commands_utils import has_support_creation_permission
from ..buttons.base_view_factory import create_base_view
from ..shared_utils.constants import COMMUNITY_SUPPORT_CHANNEL_ID, TROUBLESHOOTING_CHANNEL_ID
from ..shared_utils.enums import ThreadState
from src.shared_utils.shared_state import set_thread_state
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def register_commands(bot):
    @bot.tree.command(name="support", description="Initiate an Olympus support request.")
    @app_commands.describe(user="The user for whom a support thread is to be created (leave blank to create a support "
                                "thread for yourself. This parameter may only be used by the DCS Olympus Team.")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def support(interaction: discord.Interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user

        if user != interaction.user:
            if not has_support_creation_permission(interaction.user):
                await interaction.response.send_message(
                    "You do not have permission to create support threads for other users!",
                    ephemeral=True
                )
                return

        if interaction.channel_id != COMMUNITY_SUPPORT_CHANNEL_ID:
            correct_channel = interaction.guild.get_channel(COMMUNITY_SUPPORT_CHANNEL_ID)
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

        # Permission check
        if not interaction.guild.me.guild_permissions.create_public_threads:
            await interaction.response.send_message(
                content="I don't have permission to create threads. Please contact an administrator.",
                ephemeral=True
            )
            return

        # Channel type check
        if not isinstance(interaction.channel, (discord.TextChannel, discord.ForumChannel)):
            await interaction.response.send_message(
                content="Threads can only be created in text or forum channels.",
                ephemeral=True
            )
            return

        troubleshooting_channel_mention = f"<#{TROUBLESHOOTING_CHANNEL_ID}>"

        thread_name = f"Support for {user.name}"

        try:
            thread = await interaction.channel.create_thread(
                name=thread_name,
                auto_archive_duration=1440,
                type=discord.ChannelType.public_thread
            )
        except discord.Forbidden as e:
            logger.error(f"Forbidden error: {e}")
            await interaction.followup.send(
                content="I don't have permission to create threads. Please check channel and server settings.",
                ephemeral=True)
            return
        except discord.HTTPException as e:
            logger.error(f"HTTP error: {e}")
            await interaction.followup.send(
                content="Failed to create thread due to a network error. Please try again later.", ephemeral=True)
            return
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await interaction.followup.send(content="An unexpected error occurred. Please try again later.",
                                            ephemeral=True)
            return

        await interaction.response.send_message(
            content=f"Support thread created for {user.mention}: {thread.mention}\n"
                    f"Please upload your log files (Olympus_log.txt and dcs.log) in this thread.",
            ephemeral=True
        )

        await thread.send(
            f"{user.mention} Welcome to your support thread. Before proceeding, please ensure you have read"
            f" all the information in the {troubleshooting_channel_mention} channel. This means that you should:\n\n"
            f"Read through the [Installation Guide](https://github.com/Pax1601/DCSOlympus/wiki) to ensure you have "
            f"setup Olympus correctly.\n\n"
            f"Read through [Setup Troubleshooting](https://github.com/Pax1601/DCSOlympus/wiki/Setup-Troubleshooting) "
            f"for common issues and solutions.\n\n"
            f"Read through the [Olympus User Guide](https://github.com/Pax1601/DCSOlympus/wiki/2.-User-Guide)"
            f" to learn how to use Olympus.\n\n"
            f"If you're still having issues after trying the steps above, please provide the following information:\n"
            f"• A detailed description of your issue\n"
            f"• Your Olympus log file (located at `<DCS Instance Saved Games folder>\\Logs\\Olympus_log.txt`)\n"
            f"• Your DCS log file (located at `<DCS Instance Saved Games folder>\\Logs\\dcs.log`)\n"
            f"• Screenshots of any relevant screens or issues\n"
            f"• Any other pertinent information\n\n"
            f"Please upload your Olympus_log.txt and dcs.log files in a single message here, which are normally found"
            f" at the file paths provided above. "
            f"After uploading, someone from the DCS Olympus team will eventually get to you. If you do not provide the "
            f"log files, the DCS Olympus Team will not be notified that you have an issue. \n\n"
            f"If, after LOOKING VERY CAREFULLY, you do not have the files, please use the buttons at the bottom of "
            f"this message for the bot to take you through a basic troubleshooting flow.",
            view=create_base_view(view_type="combined", log_status="no_logs")
        )

        set_thread_state(thread.id, ThreadState.AWAITING_LOGS)

    @support.error
    async def support_error(interaction: discord.Interaction, error):
        if isinstance(error, commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"You can only use this command once per minute. Please try again in {error.retry_after:.2f} seconds.",
                ephemeral=True)
        else:
            await interaction.response.send_message("An unexpected error occurred. Please try again later.",
                                                    ephemeral=True)
