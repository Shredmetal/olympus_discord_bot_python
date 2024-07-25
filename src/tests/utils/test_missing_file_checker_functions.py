import unittest
from unittest.mock import MagicMock, patch
import discord
from ...utils.missing_file_checker_functions import check_missing_files, generate_response_message


class TestHelperFunctions(unittest.TestCase):

    def test_check_missing_files(self):
        # Mock attachments
        attachment1 = MagicMock(spec=discord.Attachment)
        attachment1.filename = "Olympus_log.txt"
        attachment2 = MagicMock(spec=discord.Attachment)
        attachment2.filename = "dcs.log"

        attachments = [attachment1, attachment2]
        required_files = ["Olympus_log.txt", "dcs.log", "missing_file.txt"]

        # Test function
        missing_files = check_missing_files(attachments, required_files)
        self.assertEqual(missing_files, ["missing_file.txt"])

    @patch('src.utils.helper_functions.get_random_gif')
    def test_generate_response_message_with_missing_files(self, mock_get_random_gif):
        mock_get_random_gif.return_value = "https://example.com/test.gif"

        missing_files = ["missing_file.txt"]
        troubleshooting_channel_mention = "<#1234567890>"

        # Test function
        response_message = generate_response_message(missing_files, troubleshooting_channel_mention)

        # Check if the response contains the expected text
        expected_text = (f"Please attach the following missing files: missing_file.txt. It's literally in the "
                         f"{troubleshooting_channel_mention} channel which you should be reading.")
        self.assertIn(expected_text, response_message)

        # Check if the response contains the mocked GIF URL
        self.assertIn("https://example.com/test.gif", response_message)

    @patch('src.utils.helper_functions.get_random_gif')
    def test_generate_response_message_without_missing_files(self, mock_get_random_gif):
        mock_get_random_gif.return_value = "https://example.com/test.gif"

        missing_files = []
        troubleshooting_channel_mention = "<#1234567890>"
        expected_text = (f"Thank you for attaching the logs! Someone from the DCS Olympus Team will assist you "
                         f"eventually. In the meantime, please check the {troubleshooting_channel_mention} channel, "
                         f"make sure you have followed the instructions there.")

        # Test function
        response_message = generate_response_message(missing_files, troubleshooting_channel_mention)

        # Check if the response contains the expected text
        self.assertIn(expected_text, response_message)

        # Check that no GIF URL is included when there are no missing files
        self.assertNotIn("http", response_message)

    @patch('src.utils.helper_functions.get_random_gif')
    def test_generate_response_message_with_none_missing_files(self, mock_get_random_gif):
        mock_get_random_gif.return_value = "https://example.com/test.gif"

        missing_files = None
        troubleshooting_channel_mention = "<#1234567890>"
        expected_text = "Please upload the required log files (Olympus_log.txt and dcs.log)."

        # Test function
        response_message = generate_response_message(missing_files, troubleshooting_channel_mention)

        # Check if the response contains the expected text
        self.assertIn(expected_text, response_message)

        # Check if the response contains the mocked GIF URL
        self.assertIn("https://example.com/test.gif", response_message)


if __name__ == '__main__':
    unittest.main()
