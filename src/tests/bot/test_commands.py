import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import discord
from discord import Interaction, ChannelType, HTTPException, TextChannel, DMChannel
from discord.ext import commands
from ...bot.commands import register_commands



class TestCommands(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.bot = MagicMock()
        self.interaction = AsyncMock(spec=Interaction)
        self.interaction.channel_id = 12345
        self.interaction.user.name = "TestUser"
        self.interaction.guild.get_channel.return_value = AsyncMock()
        self.interaction.guild.me.guild_permissions.create_public_threads = True

        self.last_message = ''

        async def mock_send_message(*args, **kwargs):
            self.last_message = args[0] if args else kwargs.get('content', '')
            return None

        self.interaction.response.send_message = AsyncMock(side_effect=mock_send_message)
        self.interaction.followup.send = AsyncMock(side_effect=mock_send_message)

        self.interaction.channel = AsyncMock(spec=TextChannel)
        self.interaction.channel.create_thread = AsyncMock()

        self.mock_command = MagicMock()
        self.mock_command.error = MagicMock()

        def command_decorator(*args, **kwargs):
            def wrapper(func):
                self.support_command = func
                self.support_command.error = self.mock_command.error
                return self.mock_command
            return wrapper

        self.bot.tree.command = command_decorator

    def test_register_commands(self):
        register_commands(self.bot)
        self.assertIsNotNone(getattr(self, 'support_command', None))

    async def test_support_command_success(self):
        register_commands(self.bot)

        with patch('src.bot.commands.COMMUNITY_SUPPORT_CHANNEL_ID', 12345), \
             patch('src.bot.commands.set_thread_state') as mock_set_thread_state:
            await self.support_command(self.interaction)

        self.interaction.channel.create_thread.assert_called_once_with(
            name="Support for TestUser",
            auto_archive_duration=1440,
            type=ChannelType.public_thread
        )
        self.interaction.response.send_message.assert_called_once()
        call_kwargs = self.interaction.response.send_message.call_args.kwargs
        self.assertIn("Support thread created", call_kwargs.get('content', ''))
        mock_set_thread_state.assert_called_once()

    async def test_support_command_thread_creation_failure(self):
        register_commands(self.bot)

        mock_response = AsyncMock()
        mock_response.status = 400
        mock_response.reason = "Bad Request"
        self.interaction.channel.create_thread.side_effect = HTTPException(mock_response, "error")

        with patch('src.bot.commands.COMMUNITY_SUPPORT_CHANNEL_ID', 12345):
            await self.support_command(self.interaction)

        self.interaction.followup.send.assert_called_once()
        call_kwargs = self.interaction.followup.send.call_args.kwargs
        self.assertIn("Failed to create thread due to a network error", call_kwargs.get('content', ''))

    async def test_support_command_wrong_channel_type(self):
        register_commands(self.bot)
        self.interaction.channel = AsyncMock(spec=DMChannel)  # or any non-TextChannel type

        with patch('src.bot.commands.COMMUNITY_SUPPORT_CHANNEL_ID', 12345):
            await self.support_command(self.interaction)

        self.interaction.response.send_message.assert_called_once()
        call_kwargs = self.interaction.response.send_message.call_args.kwargs
        self.assertIn("Threads can only be created in text or forum channels", call_kwargs.get('content', ''))

    async def test_support_error_cooldown(self):
        register_commands(self.bot)

        error = commands.CommandOnCooldown(commands.BucketType.user, 30, 60)  # 60 seconds cooldown
        error_handler = self.mock_command.error.call_args[0][0]
        await error_handler(self.interaction, error)

        self.interaction.response.send_message.assert_called_once()
        expected_message = "You can only use this command once per minute. Please try again in 30.00 seconds."
        self.assertIn(expected_message, self.last_message)

    async def test_support_error_generic(self):
        register_commands(self.bot)

        error = Exception("Generic error")
        error_handler = self.mock_command.error.call_args[0][0]
        await error_handler(self.interaction, error)

        self.interaction.response.send_message.assert_called_once()
        self.assertIn("An unexpected error occurred", self.last_message)

if __name__ == '__main__':
    unittest.main()