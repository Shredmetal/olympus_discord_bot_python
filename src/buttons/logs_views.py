import discord

from src.buttons.problem_resolution_view import ResolutionView
from src.core.shared_state import set_thread_state, get_thread_state
from src.utils.enums import ThreadState
from src.utils.constants import COMMUNITY_SUPPORT_CHANNEL_ID, THREAD_CLOSED_STRING


class InitialView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        thread_state = get_thread_state(interaction.channel.id)
        if thread_state == ThreadState.CLOSED or thread_state == ThreadState.LOGS_RECEIVED:
            await interaction.response.send_message(THREAD_CLOSED_STRING, ephemeral=True)
            return False
        return True

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
        message = ("A common issue our users experience is that DCS Olympus is not installed in the right place. You "
                   "can do so with ease through the provided Olympus Manager. Simply launch Olympus Manager and check "
                   "that DCS Olympus has been installed for the DCS Olympus instance for which you are experiencing "
                   "issues.")
        await interaction.response.send_message(message, view=ResolutionView())
