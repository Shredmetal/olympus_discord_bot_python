import discord
from typing import Literal

from src.buttons.problem_resolution_view import ResolutionView
from src.core.shared_state import get_thread_state, set_thread_state
from src.utils.enums import ThreadState
from src.utils.constants import THREAD_CLOSED_STRING, SUPPORT_REQUESTS_ID


class CommonIssuesView(discord.ui.View):
    def __init__(self,
                 resolution_type: Literal["normal", "no_logs"] = "normal"):
        super().__init__(timeout=None)
        self.resolution_type = resolution_type

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        thread_state = get_thread_state(interaction.channel.id)
        if thread_state == ThreadState.CLOSED:
            await interaction.response.send_message(THREAD_CLOSED_STRING, ephemeral=True)
            return False
        return True

    def get_resolution_view(self, manager_mentioned="yes") -> ResolutionView:
        if self.resolution_type == "no_logs" and manager_mentioned == "no":
            return ResolutionView(include_not_resolved=False, include_no_manager=False)
        elif self.resolution_type == "no_logs":
            return ResolutionView(include_not_resolved=False)
        elif manager_mentioned == "no":
            return ResolutionView(include_not_resolved_no_logs=False, include_no_manager=False)
        else:
            return ResolutionView(include_not_resolved_no_logs=False)

    @discord.ui.button(label="1", style=discord.ButtonStyle.blurple, custom_id="usr_pw")
    async def no_usr_pw(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_no_usr_pw(interaction)

    @discord.ui.button(label="2", style=discord.ButtonStyle.blurple, custom_id="stuck_connecting")
    async def stuck_connecting(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_stuck_connecting(interaction)

    @discord.ui.button(label="3", style=discord.ButtonStyle.blurple, custom_id="half_scrn_white")
    async def half_scrn_white(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_half_scrn_white(interaction)

    @discord.ui.button(label="4", style=discord.ButtonStyle.blurple, custom_id="mist_problem")
    async def mist_problem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_mist_problem(interaction)

    @discord.ui.button(label="5", style=discord.ButtonStyle.blurple,
                       custom_id="mod_aircraft")
    async def mod_aircraft_problem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_mod_aircraft_problem(interaction)

    @discord.ui.button(label="6", style=discord.ButtonStyle.blurple, custom_id="econnrefused")
    async def econnrefused(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_econnrefused(interaction)

    @discord.ui.button(label="7", style=discord.ButtonStyle.blurple, custom_id="browser_says_no")
    async def browser_says_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_browser_says_no(interaction)

    @discord.ui.button(label="8", style=discord.ButtonStyle.blurple, custom_id="problem_not_listed")
    async def problem_not_listed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_problem_not_listed(interaction)

    async def handle_no_usr_pw(self, interaction: discord.Interaction):
        message = ("You set your own username and password when running the installer. Please use Olympus Manager to "
                   "reinstall / reset your username and password. Please read everything in the installer and do not "
                   "just click 'next' to avoid similar issues in the future. The username is not important and it "
                   "is only used for logging purposes. What you need to remember / store somewhere safe is the "
                   "password.")
        await interaction.response.send_message(message, view=self.get_resolution_view())

    async def handle_stuck_connecting(self, interaction: discord.Interaction):
        message = ("Your problem is frequently caused by a port not being open. You can check this by casting the "
                   "following spell in your command line: 'netstat -an | findstr 3000'. To use the command line, "
                   "search for and run cmd from your Windows search bar. Either way, you should make sure that Windows "
                   "firewall is not blocking your Olympus port. ALSO, MAKE SURE THAT YOUR MISSION IS UNPAUSED IN-GAME. "
                   "Check [here](https://github.com/Pax1601/DCSOlympus/wiki/5.-Setup-Troubleshooting-(v1.0.3)) for "
                   "more information on how to change that. You should also try changing the ports used by Olympus "
                   "using the Olympus manager. Please make sure to try these steps to resolve your issue, or you may "
                   "be stuck waiting for one of us to help you out for quite a while.")
        await interaction.response.send_message(message, view=self.get_resolution_view())

    async def handle_half_scrn_white(self, interaction: discord.Interaction):
        message = ("This is usually caused by some browser extension. You need to try (1) using incognito mode, (2) "
                   "disabling extensions, and (3) changing to a different browser. Olympus was built with Chrome in "
                   "mind and the team does not have the time to test every other browser in existence. Additionally, "
                   "some password managers / apps may present an alert bar at the top of the page which can cause "
                   "this issue. Dismiss or close the alert and see if it solves the issue.")
        await interaction.response.send_message(message, view=self.get_resolution_view(manager_mentioned="no"))

    async def handle_mist_problem(self, interaction: discord.Interaction):
        message = ("This is usually caused by some sort of incompatibility with mist. To verify, please launch a "
                   "mission without any scripts or mods. This is frequently caused by Pretense, amongst others.")
        await interaction.response.send_message(message, view=self.get_resolution_view(manager_mentioned="no"))

    async def handle_mod_aircraft_problem(self, interaction: discord.Interaction):
        message = ("We do not include mod aircraft by default as not everyone has the same mods installed. However, "
                   "there is a way to add them, please follow the instructions in the documentation "
                   "[here](https://github.com/Pax1601/DCSOlympus/wiki/2.-User-Guide#adding-mods-to-the-database). "
                   "We recommend that you do not try this if you have absolutely no familiarity with code at all. "
                   "Ask a friend who can talk to computers or something.")
        await interaction.response.send_message(message, view=self.get_resolution_view(manager_mentioned="no"))

    async def handle_econnrefused(self, interaction: discord.Interaction):
        message = ("You did not use netsh to remove a URL reservation. \n\nThis was specified in the installation "
                   "instructions. Either way, in DCS Olympus v1.0.4, we have removed the need to use the netsh spell "
                   "in your command line spellcasting interface, however, you will need to remove it if you have done "
                   "so previously. Please follow the instructions "
                   "[here](https://github.com/Pax1601/DCSOlympus/wiki#123-removing-the-net-shell-netsh-rule).")
        await interaction.response.send_message(message, view=self.get_resolution_view(manager_mentioned="no"))

    async def handle_browser_says_no(self, interaction: discord.Interaction):
        message = ("There could be several causes of this:\n\n"
                   "\t1. You did not start Olympus server up. If you don't see the Olympus server black command text "
                   "screen, you didn't start it up.\n"
                   "\t2. Olympus server is still starting up. Give it a few minutes and wait until you start seeing "
                   "lines being printed to the Olympus server screen.\n"
                   "\t3. You are connecting to the wrong URL. Check your Olympus manager ")
        await interaction.response.send_message(message, view=self.get_resolution_view())

    async def handle_browser_says_no(self, interaction: discord.Interaction):
        thread_state = get_thread_state(interaction.channel.id)
        support_requests_channel = interaction.client.get_channel(SUPPORT_REQUESTS_ID)
        if support_requests_channel:
            if thread_state == ThreadState.LOGS_RECEIVED:
                await support_requests_channel.send(f"Unresolved issue in thread: {interaction.channel.mention}, user "
                                                    f"has provided logs.")
            else:
                await support_requests_channel.send(f"Unresolved issue in thread: {interaction.channel.mention}, user "
                                                    f"has not provided logs.")
        await interaction.response.send_message("The DCS Olympus team has been notified and one of us will be with"
                                                " you to look into this eventually.")
        set_thread_state(interaction.channel.id, ThreadState.CLOSED)
