import discord

from typing import Literal

from src.buttons.common_issues_buttons.common_issues_list_view import CommonIssuesListView
from src.buttons.logs_view import InitialView
from src.core.shared_state import get_thread_state
from src.main_utils.constants import THREAD_CLOSED_STRING
from src.main_utils.enums import ThreadState


class BaseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        thread_state = get_thread_state(interaction.channel.id)
        if thread_state == ThreadState.CLOSED:
            await interaction.response.send_message(THREAD_CLOSED_STRING, ephemeral=True)
            return False
        return True


def create_base_view(view_type: Literal["initial", "common_issues", "combined"],
                     log_status: Literal["normal", "no_logs"] = "normal") -> BaseView:
    if view_type == "initial":
        return InitialView()
    elif view_type == "common_issues":
        return CommonIssuesListView(log_status=log_status)
    elif view_type == "combined":
        view = InitialView()

        common_issues_button = discord.ui.Button(
            label="List of common issues and troubleshooting steps",
            style=discord.ButtonStyle.blurple,
            custom_id="common_issues_list"
        )

        common_issues_button.callback = CommonIssuesListView(log_status=log_status).common_issues_list.callback

        view.add_item(common_issues_button)
        return view
    else:
        raise ValueError(f"Invalid view_type: {view_type}")
