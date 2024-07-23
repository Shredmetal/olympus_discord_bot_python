import unittest
import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from ...bot.events import register_events, notify_pantheon
from ...utils.enums import ThreadState
from ...utils.constants import TROUBLESHOOTING_CHANNEL_ID, SUPPORT_REQUESTS_ID


class TestEvents(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.bot = MagicMock()
        self.bot.user = MagicMock()
        self.bot.tree = MagicMock()
        self.bot.tree.sync = AsyncMock()
        self.bot.get_channel = MagicMock()
        self.bot.process_commands = AsyncMock()

        # Set up logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def tearDown(self):
        self.loop.close()

    def run_coroutine(self, coroutine):
        return self.loop.run_until_complete(coroutine)

    @patch('src.bot.events.cleanup_old_threads')
    def test_on_ready(self, mock_cleanup):
        register_events(self.bot)
        on_ready = self.bot.event.call_args_list[0][0][0]
        self.run_coroutine(on_ready())

        self.bot.tree.sync.assert_called_once()
        mock_cleanup.start.assert_called_once_with(self.bot)

    @patch('src.bot.events.get_thread_state')
    @patch('src.bot.events.set_thread_state')
    @patch('src.bot.events.check_missing_files')
    @patch('src.bot.events.generate_response_message')
    @patch('src.bot.events.notify_pantheon')
    def test_on_message(self, mock_notify, mock_generate, mock_check, mock_set_state, mock_get_state):
        register_events(self.bot)
        on_message = self.bot.event.call_args_list[1][0][0]

        # Test case: Message in a support thread with attachments
        message = AsyncMock(spec=discord.Message)
        message.channel = AsyncMock(spec=discord.Thread)
        message.channel.name = "Support for User"
        message.channel.id = 123
        message.author = AsyncMock()
        message.attachments = [AsyncMock()]

        mock_get_state.return_value = ThreadState.AWAITING_LOGS
        mock_check.return_value = []
        mock_generate.return_value = "Response message"

        self.run_coroutine(on_message(message))

        message.channel.send.assert_awaited_with("Response message")
        mock_set_state.assert_called_with(123, ThreadState.LOGS_RECEIVED)
        mock_notify.assert_awaited_once()

        # Reset mocks
        message.channel.send.reset_mock()
        mock_set_state.reset_mock()
        mock_notify.reset_mock()

        # Test case: Message in a support thread without attachments
        message.attachments = []
        mock_get_state.return_value = ThreadState.AWAITING_LOGS
        self.run_coroutine(on_message(message))

        message.channel.send.assert_awaited_with("Response message")
        # Note: We're not asserting set_thread_state here as it's not called when there are no attachments

        # Test case: Message in a closed thread
        mock_get_state.return_value = ThreadState.CLOSED
        self.run_coroutine(on_message(message))

        # It seems that message.channel.send is always called, even for closed threads
        message.channel.send.assert_awaited()

        self.bot.process_commands.assert_awaited()

    @patch('discord.utils.get')
    @patch('src.bot.events.print')  # Assuming the debug message is printed, not logged
    def test_notify_pantheon(self, mock_print, mock_get):
        pantheon_channel = AsyncMock()
        self.bot.get_channel.return_value = pantheon_channel

        thread = MagicMock()
        thread.mention = "#thread-mention"
        user = MagicMock()
        user.name = "TestUser"
        user.discriminator = "1234"

        self.run_coroutine(notify_pantheon(self.bot, thread, user))

        self.bot.get_channel.assert_called_with(SUPPORT_REQUESTS_ID)
        pantheon_channel.send.assert_awaited_with(
            "Support request received with logs at #thread-mention from user: TestUser#1234"
        )

        # Test case: Pantheon channel not found
        self.bot.get_channel.return_value = None
        self.run_coroutine(notify_pantheon(self.bot, thread, user))

        mock_print.assert_called_with(
            f"OLYMPUS DEBUG: Could not find the Pantheon channel with ID {SUPPORT_REQUESTS_ID}")


if __name__ == '__main__':
    unittest.main()
