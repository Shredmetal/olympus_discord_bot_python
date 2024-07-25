import unittest
from unittest.mock import MagicMock, patch
import discord
from src.bot.events_utils.missing_file_checker_functions import check_missing_files, generate_response_message
from src.shared_utils.enums import ThreadState

class TestHelperFunctions(unittest.TestCase):

    def test_check_missing_files(self):
        # This test case remains the same as the function hasn't changed
        attachment1 = MagicMock(spec=discord.Attachment)
        attachment1.filename = "Olympus_log.txt"
        attachment2 = MagicMock(spec=discord.Attachment)
        attachment2.filename = "dcs.log"

        attachments = [attachment1, attachment2]
        required_files = ["Olympus_log.txt", "dcs.log", "missing_file.txt"]

        missing_files = check_missing_files(attachments, required_files)
        self.assertEqual(missing_files, ["missing_file.txt"])

    @patch('src.bot.events_utils.missing_file_checker_functions.get_random_gif')
    def test_generate_response_message_with_missing_files(self, mock_get_random_gif):
        mock_get_random_gif.return_value = "https://example.com/test.gif"

        missing_files = ["missing_file.txt"]
        troubleshooting_channel_mention = "<#1234567890>"
        thread_state = ThreadState.AWAITING_LOGS

        response_message = generate_response_message(missing_files, troubleshooting_channel_mention, thread_state)

        expected_text = "Please attach the following missing files: missing_file.txt. Please attach them to a single message."
        self.assertIn(expected_text, response_message)
        self.assertIn("https://example.com/test.gif", response_message)

    @patch('src.bot.events_utils.missing_file_checker_functions.get_random_gif')
    def test_generate_response_message_without_missing_files(self, mock_get_random_gif):
        mock_get_random_gif.return_value = "https://example.com/test.gif"

        missing_files = []
        troubleshooting_channel_mention = "<#1234567890>"
        thread_state = ThreadState.AWAITING_LOGS

        response_message = generate_response_message(missing_files, troubleshooting_channel_mention, thread_state)

        expected_text = "Thank you for attaching the logs! We will get to you eventually"
        self.assertIn(expected_text, response_message)
        self.assertIn(troubleshooting_channel_mention, response_message)
        self.assertNotIn("https://example.com/test.gif", response_message)

    @patch('src.bot.events_utils.missing_file_checker_functions.get_random_gif')
    def test_generate_response_message_with_none_missing_files_awaiting_logs(self, mock_get_random_gif):
        mock_get_random_gif.return_value = "https://example.com/test.gif"

        missing_files = None
        troubleshooting_channel_mention = "<#1234567890>"
        thread_state = ThreadState.AWAITING_LOGS

        response_message = generate_response_message(missing_files, troubleshooting_channel_mention, thread_state)

        expected_text = "Please upload the required log files (Olympus_log.txt and dcs.log) in a single message."
        self.assertIn(expected_text, response_message)
        self.assertIn("https://example.com/test.gif", response_message)

    @patch('src.bot.events_utils.missing_file_checker_functions.get_random_gif')
    def test_generate_response_message_with_none_missing_files_no_olympus_logs(self, mock_get_random_gif):
        mock_get_random_gif.return_value = "https://example.com/test.gif"

        missing_files = None
        troubleshooting_channel_mention = "<#1234567890>"
        thread_state = ThreadState.NO_OLYMPUS_LOGS

        response_message = generate_response_message(missing_files, troubleshooting_channel_mention, thread_state)

        expected_text = "Please upload the required log files (dcs.log)"
        self.assertIn(expected_text, response_message)
        self.assertIn("https://example.com/test.gif", response_message)


if __name__ == '__main__':
    unittest.main()