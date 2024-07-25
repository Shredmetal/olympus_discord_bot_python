import discord

from src.buttons.base_view import BaseView, create_base_view
from src.main_utils.shared_state import set_thread_state
from src.main_utils.enums import ThreadState
from src.main_utils.constants import COMMUNITY_SUPPORT_CHANNEL_ID
from src.main_utils.online_resources import get_random_gif


class InitialView(BaseView):
    @discord.ui.button(label="I do not have dcs.log", style=discord.ButtonStyle.red, custom_id="no_dcs_log")
    async def no_dcs_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_no_dcs_log(interaction)

    @discord.ui.button(label="I do not have Olympus_log.txt", style=discord.ButtonStyle.red, custom_id="no_olympus_log")
    async def no_olympus_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_no_olympus_log(interaction)

    @discord.ui.button(label="I do not have either log file", style=discord.ButtonStyle.red, custom_id="no_both_logs")
    async def no_both_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_no_dcs_log(interaction)

    async def handle_no_dcs_log(self, interaction: discord.Interaction):
        message = (f"If you do not have dcs.log, you do not have DCS installed. DCS Olympus is a mod for DCS. "
                   f"If you do not have DCS installed, then you are not able to use DCS Olympus. Please ensure that "
                   f"you have installed DCS, and follow the DCS Olympus setup instructions carefully. This thread will "
                   f"now be closed. If you experience issues thereafter, please use the '/support' command in the "
                   f"<#{COMMUNITY_SUPPORT_CHANNEL_ID}> channel again")
        await interaction.response.send_message(message)
        set_thread_state(interaction.channel.id, ThreadState.CLOSED)
        await interaction.channel.edit(archived=True)

    async def handle_no_olympus_log(self, interaction: discord.Interaction):
        random_gif = get_random_gif()
        message = ("A common issue our users experience is that DCS Olympus is not installed in the right place. You "
                   "can do so with ease through the provided Olympus Manager. Simply launch Olympus Manager and check "
                   "that DCS Olympus has been installed for the DCS Olympus instance for which you are experiencing "
                   "issues. Please send us all your dcs.logs anyway to help us resolve your problem. Even if the "
                   "dcs.log is for another DCS instance. In the meantime, please look through the common issues list "
                   "by clicking on the list of common issues button below. The bot will keep harassing you for the "
                   "dcs.log until you upload it, so please upload it as soon as possible. If you don't have the "
                   "dcs.log, please state so using the provided button for guidance."
                   f"{random_gif}")
        set_thread_state(interaction.channel.id, ThreadState.NO_OLYMPUS_LOGS)
        await interaction.response.send_message(message,
                                                view=create_base_view(
                                                    view_type="combined",
                                                    log_status="no_logs"))
