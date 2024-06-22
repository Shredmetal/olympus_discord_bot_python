import unittest
from unittest.mock import MagicMock
import discord
from helper_functions import check_missing_files, generate_response_message

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

    def test_generate_response_message_with_missing_files(self):
        missing_files = ["missing_file.txt"]
        troubleshooting_channel_mention = "<#1234567890>"
        expected_message = "Please attach the following missing files: missing_file.txt. It's literally in the <#1234567890> channel which you should be reading."

        # Test function
        response_message = generate_response_message(missing_files, troubleshooting_channel_mention)
        self.assertEqual(response_message, expected_message)

    def test_generate_response_message_without_missing_files(self):
        missing_files = []
        troubleshooting_channel_mention = "<#1234567890>"
        expected_message = "Thank you for attaching the logs! Someone from the DCS Olympus Team will assist you eventually. In the meantime, please check the <#1234567890> channel and read everything there to ensure you have followed the instructions."

        # Test function
        response_message = generate_response_message(missing_files, troubleshooting_channel_mention)
        self.assertEqual(response_message, expected_message)

if __name__ == '__main__':
    unittest.main()
