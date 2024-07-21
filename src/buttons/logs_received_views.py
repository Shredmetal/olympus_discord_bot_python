import discord

from src.buttons.problem_resolution_view import ResolutionView
from src.core.shared_state import set_thread_state, get_thread_state
from src.utils.enums import ThreadState
from src.utils.constants import PANTHEON_CHANNEL_ID, COMMUNITY_SUPPORT_CHANNEL_ID, THREAD_CLOSED_STRING


class LogsReceivedView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        thread_state = get_thread_state(interaction.channel.id)
        if thread_state == ThreadState.CLOSED:
            await interaction.response.send_message(THREAD_CLOSED_STRING, ephemeral=True)
            return False
        return True

    @discord.ui.button(label="I don't know my Username / Password", style=discord.ButtonStyle.blurple, custom_id="usr_pw")
    async def no_usr_pw(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_no_usr_pw(interaction)

    @discord.ui.button(label="Olympus stuck on connecting", style=discord.ButtonStyle.blurple, custom_id="stuck_connecting")
    async def stuck_connecting(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_stuck_connecting(interaction)

    @discord.ui.button(label="Half the screen is white", style=discord.ButtonStyle.blurple, custom_id="half_scrn_white")
    async def half_scrn_white(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_half_scrn_white(interaction)

    async def handle_no_usr_pw(self, interaction: discord.Interaction):
        message = ("You set your own username and password when running the installer. Please use Olympus Manager to "
                   "reinstall / reset your username and password. Please read everything in the installer and do not "
                   "just click 'next' to avoid similar issues in the future. The username is not important and it "
                   "is only used for logging purposes. What you need to remember / store somewhere safe is the "
                   "password.")
        await interaction.response.send_message(message, view=ResolutionView())

    async def handle_stuck_connecting(self, interaction: discord.Interaction):
        message = ("Your problem is frequently caused by a port not being open. You can check this by casting the "
                   "following spell in your command line: 'netstat -an | findstr 3000'. To use the command line, "
                   "search for and run cmd from your Windows search bar. Either way, you should make sure that Windows "
                   "firewall is not blocking your Olympus port. "
                   "Check [here](https://github.com/Pax1601/DCSOlympus/wiki/5.-Setup-Troubleshooting-(v1.0.3)) for "
                   "more information on how to change that. You should also try changing the ports used by Olympus "
                   "using the Olympus manager. Please make sure to try these steps to resolve your issue, or you may "
                   "be stuck waiting for one of us to help you out for quite a while.")
        await interaction.response.send_message(message, view=ResolutionView())

    async def handle_half_scrn_white(self, interaction: discord.Interaction):
        message = ("This is usually caused by some browser extension. You need to try (1) using incognito mode, (2) "
                   "disabling extensions, and (3) changing to a different browser. Olympus was built with Chrome in "
                   "mind and the team does not have the time to test every other browser in existence. Additionally, "
                   "some password managers / apps may present an alert bar at the top of the page which can cause "
                   "this issue. Dismiss or close the alert and see if it solves the issue.")
        await interaction.response.send_message(message, view=ResolutionView())
