import discord

from src.core.shared_state import get_thread_state, set_thread_state
from src.utils.constants import THREAD_CLOSED_STRING, SUPPORT_REQUESTS_ID
from src.utils.enums import ThreadState


class ResolutionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        thread_state = get_thread_state(interaction.channel.id)
        if thread_state == ThreadState.CLOSED:
            await interaction.response.send_message(THREAD_CLOSED_STRING, ephemeral=True)
            return False
        return True

    @discord.ui.button(label="That resolved my issue", style=discord.ButtonStyle.green, custom_id="issue_resolved")
    async def issue_resolved(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Great! Glad we could help. This thread will now be closed.")
        set_thread_state(interaction.channel.id, ThreadState.CLOSED)
        await interaction.channel.edit(archived=True)

    @discord.ui.button(label="That did not resolve my issue", style=discord.ButtonStyle.red, custom_id="issue_not_resolved")
    async def issue_not_resolved(self, interaction: discord.Interaction, button: discord.ui.Button):
        pantheon_channel = interaction.client.get_channel(SUPPORT_REQUESTS_ID)
        if pantheon_channel:
            await pantheon_channel.send(f"Unresolved issue in thread: {interaction.channel.mention}")
        await interaction.response.send_message("The DCS Olympus team has been notified and one of us will be with"
                                                " you to look into this eventually.")
        set_thread_state(interaction.channel.id, ThreadState.CLOSED)

    @discord.ui.button(label="I don't have olympus manager!", style=discord.ButtonStyle.blurple, custom_id="no_manager")
    async def no_olympus_manager(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = ("Olympus Manager was introduced with DCS Olympus v1.0.4. It simplifies the installation and "
                   "uninstallation process. So please, for the love of god, update your DCS Olympus. As usual, it is "
                   "available on our releases page [here](https://github.com/Pax1601/DCSOlympus/releases)! It allows "
                   "you to manage one or more DCS Olympus installations, which you may need if you have both the DCS "
                   "client and a DCS Server installed. If you installed DCS Olympus prior to v1.0.4, please uninstall "
                   "it using using 'Add/Remove Programs' in Windows and reinstall it using the Olympus Manager "
                   "provided with v1.0.4")
        await interaction.response.send_message(message, view=ResolutionView())
