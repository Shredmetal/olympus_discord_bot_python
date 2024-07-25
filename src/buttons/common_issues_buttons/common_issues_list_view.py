import discord
from typing import Literal

from src.buttons.common_issues_buttons.common_issues_view import CommonIssuesView
from src.buttons.base_view import BaseView


class CommonIssuesListView(BaseView):
    def __init__(self, log_status: Literal["normal", "no_logs"] = "normal"):
        super().__init__()
        self.log_status = log_status

    @discord.ui.button(label="List of common issues and troubleshooting steps",
                       style=discord.ButtonStyle.blurple,
                       custom_id="common_issues_list")
    async def common_issues_list(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_common_issues_list(interaction)

    async def show_common_issues_list(self, interaction: discord.Interaction):
        message = ("Here is a list of common issues that our users typically face, please select "
                   "the corresponding numbered button if that is what you are facing:\n\n"
                   "\t1. I don't know my username / password\n"
                   "\t2. I entered my username and password but Olympus is stuck on 'connecting'\n"
                   "\t3. I am logged into Olympus but half of my browser's screen is white\n"
                   "\t4. I am logged into Olympus and can see units moving, but can't create any\n"
                   "\t5. I do not see aircraft I got from a mod in my unit spawn list\n"
                   "\t6. Olympus isn't working, I have the Olympus server screen (black and white with text) and I "
                   "see the word [ECONNREFUSED] on it\n"
                   "\t7. I am navigating to what I think is the correct URL but the browser tells me it cannot resolve "
                   "the URL, or that it can't find it, or something of that sort\n"
                   "\t8. My issue is not listed\n")
        await interaction.response.send_message(message, view=CommonIssuesView(resolution_type=self.log_status))
