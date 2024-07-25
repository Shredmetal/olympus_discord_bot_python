import unittest
import asyncio
import logging

from unittest.mock import AsyncMock, MagicMock, patch
import discord
from src.bot.events import register_events
from src.shared_utils.enums import ThreadState
from src.shared_utils.constants import SUPPORT_REQUESTS_ID
from src.bot.events_utils.events_utils import notify_support_requests


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
    @patch('src.bot.events.handle_awaiting_logs')
    @patch('src.bot.events.handle_no_olympus_logs')
    def test_on_message(self, mock_handle_no_olympus_logs, mock_handle_awaiting_logs, mock_set_state, mock_get_state):
        register_events(self.bot)
        on_message = self.bot.event.call_args_list[1][0][0]

        # Create a message mock
        message = AsyncMock(spec=discord.Message)
        message.channel = AsyncMock(spec=discord.Thread)
        message.channel.name = "Support for User"
        message.channel.id = 123
        message.author = AsyncMock()
        message.author.bot = False

        # Test case: Message in a support thread with AWAITING_LOGS state
        mock_get_state.return_value = ThreadState.AWAITING_LOGS
        self.run_coroutine(on_message(message))
        mock_handle_awaiting_logs.assert_awaited_once_with(message, 123, ThreadState.AWAITING_LOGS, self.bot)
        mock_handle_no_olympus_logs.assert_not_called()

        # Reset mocks
        mock_handle_awaiting_logs.reset_mock()
        mock_handle_no_olympus_logs.reset_mock()

        # Test case: Message in a support thread with NO_OLYMPUS_LOGS state
        mock_get_state.return_value = ThreadState.NO_OLYMPUS_LOGS
        self.run_coroutine(on_message(message))
        mock_handle_no_olympus_logs.assert_awaited_once_with(message, 123, ThreadState.NO_OLYMPUS_LOGS, self.bot)
        mock_handle_awaiting_logs.assert_not_called()

        # Reset mocks
        mock_handle_awaiting_logs.reset_mock()
        mock_handle_no_olympus_logs.reset_mock()

        # Test case: Message in a closed thread
        mock_get_state.return_value = ThreadState.CLOSED
        self.run_coroutine(on_message(message))
        mock_handle_awaiting_logs.assert_not_called()
        mock_handle_no_olympus_logs.assert_not_called()

        # Test case: Message in a thread with LOGS_RECEIVED state
        mock_get_state.return_value = ThreadState.LOGS_RECEIVED
        self.run_coroutine(on_message(message))
        mock_handle_awaiting_logs.assert_not_called()
        mock_handle_no_olympus_logs.assert_not_called()

        self.bot.process_commands.assert_awaited()

    @patch('src.bot.events_utils.events_utils.print')
    def test_notify_support_requests(self, mock_print):
        pantheon_channel = AsyncMock()
        self.bot.get_channel.return_value = pantheon_channel

        thread = MagicMock()
        thread.mention = "#thread-mention"
        user = MagicMock()
        user.name = "TestUser"
        user.discriminator = "1234"

        self.run_coroutine(notify_support_requests(self.bot, thread, user))

        self.bot.get_channel.assert_called_with(SUPPORT_REQUESTS_ID)
        pantheon_channel.send.assert_awaited_with(
            "Support request received with logs at #thread-mention from user: TestUser#1234"
        )

        # Test case: Pantheon channel not found
        self.bot.get_channel.return_value = None
        self.run_coroutine(notify_support_requests(self.bot, thread, user))

        mock_print.assert_called_with(
            f"OLYMPUS DEBUG: Could not find the Pantheon channel with ID {SUPPORT_REQUESTS_ID}")


if __name__ == '__main__':
    unittest.main()
