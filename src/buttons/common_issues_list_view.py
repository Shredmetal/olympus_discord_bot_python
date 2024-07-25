import discord
from typing import Literal

from src.buttons.common_issues_view import CommonIssuesView
from src.core.shared_state import get_thread_state
from src.utils.enums import ThreadState
from src.utils.constants import THREAD_CLOSED_STRING


class CommonIssuesListView(discord.ui.View):
    def __init__(self, log_status: Literal["normal", "no_logs"] = "normal"):
        super().__init__(timeout=None)
        self.resolution_type = log_status

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        thread_state = get_thread_state(interaction.channel.id)
        if thread_state == ThreadState.CLOSED:
            await interaction.response.send_message(THREAD_CLOSED_STRING, ephemeral=True)
            return False
        return True

    def get_common_issues_view(self) -> CommonIssuesView:
        if self.resolution_type == 'no_logs':
            return CommonIssuesView(resolution_type="no_logs")
        else:
            return CommonIssuesView(resolution_type="normal")

    @discord.ui.button(label="List of common issues and troubleshooting steps",
                       style=discord.ButtonStyle.blurple,
                       custom_id="common_issues_list")
    async def common_issues_list(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_common_issues_list(interaction)

    async def handle_no_usr_pw(self, interaction: discord.Interaction):
        message = ("Here is a list of common issues that our users typically face, please select "
                   "the corresponding numbered button if that is what you are facing:\n\n"
                   "\t1. I don't know my username / password\n"
                   "\t2. I entered my username and password but Olympus is stuck on 'connecting'\n"
                   "\t3. I am logged into Olympus but half of my browser's screen is white\n"
                   "\t4. I am logged into Olympus and can see units moving, but can't create any\n"
                   "\t5. I do not see aircraft I got from a mod in my unit spawn list\n"
                   "\t6. Olympus isn't working, I have the Olympus server screen (black and white with text) and I "
                   "see the word [ECONNREFUSED] on it\n")
        await interaction.response.send_message(message, view=self.get_common_issues_view())