import discord
from ..core.shared_state import set_thread_state, get_thread_state
from ..utils.enums import ThreadState
from ..utils.constants import PANTHEON_CHANNEL_ID, COMMUNITY_SUPPORT_CHANNEL_ID, THREAD_CLOSED_STRING


class LogOptionsView(discord.ui.View):
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
        pantheon_channel = interaction.client.get_channel(PANTHEON_CHANNEL_ID)
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
