import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from discord import Interaction, HTTPException
from discord.ext import commands
from ...bot.commands import register_commands


class TestCommands(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.bot = MagicMock()
        self.interaction = AsyncMock(spec=Interaction)
        self.interaction.channel_id = 12345  # Set this to match COMMUNITY_SUPPORT_CHANNEL_ID for valid tests
        self.interaction.user.name = "TestUser"
        self.interaction.guild.get_channel.return_value = AsyncMock()

        self.last_message = ''  # Initialize last_message

        # Create a more sophisticated mock for send_message
        async def mock_send_message(*args, **kwargs):
            self.last_message = args[0] if args else kwargs.get('content', '')
            return None

        self.interaction.response.send_message = AsyncMock(side_effect=mock_send_message)

        self.interaction.channel.create_thread = AsyncMock()

        # Create a mock command
        self.mock_command = MagicMock()
        self.mock_command.error = MagicMock()

        # Mock the bot.tree.command decorator
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

        self.interaction.channel.create_thread.assert_called_once()
        self.interaction.response.send_message.assert_called_once()
        call_kwargs = self.interaction.response.send_message.call_args.kwargs
        self.assertIn("Support thread created", call_kwargs.get('content', ''))
        mock_set_thread_state.assert_called_once()

    async def test_support_command_thread_creation_failure(self):
        register_commands(self.bot)

        self.interaction.channel.create_thread.side_effect = HTTPException(AsyncMock(), 'error')

        with patch('src.bot.commands.COMMUNITY_SUPPORT_CHANNEL_ID', 12345):
            await self.support_command(self.interaction)

        self.interaction.response.send_message.assert_called_once()
        call_kwargs = self.interaction.response.send_message.call_args.kwargs
        self.assertIn("Failed to create support thread", call_kwargs.get('content', ''))

    async def test_support_command_wrong_channel(self):
        register_commands(self.bot)

        with patch('src.bot.commands.COMMUNITY_SUPPORT_CHANNEL_ID', 54321):
            await self.support_command(self.interaction)

        self.interaction.response.send_message.assert_called_once()
        self.assertIn("This command can only be used in the designated support channel", self.last_message)

    async def test_support_error_cooldown(self):
        register_commands(self.bot)

        error = commands.CommandOnCooldown(commands.BucketType.user, 30, 3600)  # Added retry_after parameter
        error_handler = self.mock_command.error.call_args[0][0]
        await error_handler(self.interaction, error)

        self.interaction.response.send_message.assert_called_once()
        self.assertIn("You can only use this command once per hour", self.last_message)

    async def test_support_error_generic(self):
        register_commands(self.bot)

        error = Exception("Generic error")
        error_handler = self.mock_command.error.call_args[0][0]
        await error_handler(self.interaction, error)

        self.interaction.response.send_message.assert_called_once()
        self.assertIn("An unexpected error occurred", self.last_message)

if __name__ == '__main__':
    unittest.main()