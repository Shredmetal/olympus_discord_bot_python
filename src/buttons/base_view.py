import discord

from src.shared_utils.shared_state import get_thread_state
from src.shared_utils.constants import THREAD_CLOSED_STRING
from src.shared_utils.enums import ThreadState


class BaseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        thread_state = get_thread_state(interaction.channel.id)
        if thread_state == ThreadState.CLOSED:
            await interaction.response.send_message(THREAD_CLOSED_STRING, ephemeral=True)
            return False
        return True
