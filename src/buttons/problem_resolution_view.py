import discord
from src.shared_utils.shared_state import get_thread_state, set_thread_state
from src.shared_utils.constants import THREAD_CLOSED_STRING, SUPPORT_REQUESTS_ID, COMMUNITY_SUPPORT_CHANNEL_ID
from src.shared_utils.enums import ThreadState
from src.shared_utils.online_resources import get_random_gif


class ResolutionView(discord.ui.View):
    def __init__(self,
                 include_resolved=True,
                 include_not_resolved=True,
                 include_no_manager=True,
                 include_not_resolved_no_logs=True):
        super().__init__(timeout=None)

        if include_resolved:
            self.issue_resolved_button = discord.ui.Button(label="That resolved my issue",
                                                           style=discord.ButtonStyle.green,
                                                           custom_id="issue_resolved")
            self.issue_resolved_button.callback = self.issue_resolved
            self.add_item(self.issue_resolved_button)

        if include_not_resolved:
            self.issue_not_resolved_button = discord.ui.Button(label="That did not resolve my issue",
                                                               style=discord.ButtonStyle.red,
                                                               custom_id="issue_not_resolved")
            self.issue_not_resolved_button.callback = self.issue_not_resolved
            self.add_item(self.issue_not_resolved_button)

        if include_no_manager:
            self.no_manager_button = discord.ui.Button(label="I don't have olympus manager!",
                                                       style=discord.ButtonStyle.blurple,
                                                       custom_id="no_manager")
            self.no_manager_button.callback = self.no_olympus_manager
            self.add_item(self.no_manager_button)

        if include_not_resolved_no_logs:
            self.not_resolved_no_logs_button = discord.ui.Button(
                label="That did not resolve my issue, and I don't have one or both logs",
                style=discord.ButtonStyle.red,
                custom_id="issue_not_resolved_no_olympus_log")
            self.not_resolved_no_logs_button.callback = self.issue_not_resolved_no_logs
            self.add_item(self.not_resolved_no_logs_button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        thread_state = get_thread_state(interaction.channel.id)
        if thread_state == ThreadState.CLOSED:
            await interaction.response.send_message(THREAD_CLOSED_STRING, ephemeral=True)
            return False
        return True

    async def issue_resolved(self, interaction: discord.Interaction):
        await interaction.response.send_message("Great! Glad we could help. This thread will now be closed.")
        set_thread_state(interaction.channel.id, ThreadState.CLOSED)
        await interaction.channel.edit(archived=True)

    async def issue_not_resolved(self, interaction: discord.Interaction):
        support_requests_channel = interaction.client.get_channel(SUPPORT_REQUESTS_ID)
        if support_requests_channel:
            await support_requests_channel.send(
                f"Unresolved issue in thread: {interaction.channel.mention}, user has provided logs.")
        await interaction.response.send_message(
            "The DCS Olympus team has been notified and one of us will be with you to look into this eventually.")
        set_thread_state(interaction.channel.id, ThreadState.CLOSED)

    async def no_olympus_manager(self, interaction: discord.Interaction):
        community_support_channel = interaction.client.get_channel(COMMUNITY_SUPPORT_CHANNEL_ID)
        message = (f"Olympus Manager was introduced with DCS Olympus v1.0.4. It simplifies the installation and "
                   f"uninstallation process. So please, for the love of god, update your DCS Olympus. As usual, it is "
                   f"available on our releases page [here](https://github.com/Pax1601/DCSOlympus/releases)! It allows "
                   f"you to manage one or more DCS Olympus installations, which you may need if you have both the DCS "
                   f"client and a DCS Server installed. If you installed DCS Olympus prior to v1.0.4, please uninstall "
                   f"it using using 'Add/Remove Programs' in Windows and reinstall it using the Olympus Manager "
                   f"provided with v1.0.4. This thread will now be closed, if you have issues after installing and "
                   f"using Olympus Manager, please use /support in {community_support_channel} again.")
        await interaction.response.send_message(message)
        set_thread_state(interaction.channel.id, ThreadState.CLOSED)

    async def issue_not_resolved_no_logs(self, interaction: discord.Interaction):
        support_requests_channel = interaction.client.get_channel(SUPPORT_REQUESTS_ID)
        thread_state = get_thread_state(interaction.channel.id)
        random_gif = get_random_gif()
        if support_requests_channel:
            if thread_state == ThreadState.DCS_LOG_RECEIVED_USER_NO_OLYMPUS_LOG:
                await support_requests_channel.send(
                    f"Unresolved issue in thread: {interaction.channel.mention}, user has provided dcs.log but no Olympus_log.txt.")
            else:
                await support_requests_channel.send(
                    f"Unresolved issue in thread: {interaction.channel.mention}, user has no logs.")
        await interaction.response.send_message(
            f"The DCS Olympus team has been notified and one of us will be with you to look into this eventually. In the meantime, please upload your dcs.log. {random_gif}")
        set_thread_state(interaction.channel.id, ThreadState.CLOSED)