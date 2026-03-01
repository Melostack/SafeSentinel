import unittest
import sys
import os

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.gatekeeper import Gatekeeper

class TestGatekeeper(unittest.TestCase):
    def setUp(self):
        # Instantiate Gatekeeper with dummy paths to avoid file I/O
        # Since files don't exist, it will initialize empty registry and blacklist
        self.gk = Gatekeeper(registry_path='dummy_reg.json', blacklist_path='dummy_bl.json')

        # Manually set up a known blacklist for testing
        self.gk.blacklist = [
            {
                "address": "0xBadGuy123",
                "description": "Phishing Scam",
                "threat_type": "High"
            },
            {
                "address": "0xAnotherBadGuy",
                "description": "Malware Distribution",
                "threat_type": "Medium"
            }
        ]

    def test_check_blacklist_found(self):
        """Test that a blacklisted address is correctly identified."""
        address = "0xBadGuy123"
        result = self.gk.check_blacklist(address)
        self.assertIsNotNone(result)
        self.assertEqual(result['address'], "0xBadGuy123")
        self.assertEqual(result['description'], "Phishing Scam")

    def test_check_blacklist_not_found(self):
        """Test that a non-blacklisted address returns None."""
        address = "0xGoodGuy456"
        result = self.gk.check_blacklist(address)
        self.assertIsNone(result)

    def test_check_blacklist_case_insensitive(self):
        """Test that blacklist check is case-insensitive."""
        address_lower = "0xbadguy123"
        address_upper = "0XBADGUY123"

        result_lower = self.gk.check_blacklist(address_lower)
        self.assertIsNotNone(result_lower)
        self.assertEqual(result_lower['address'], "0xBadGuy123")

        result_upper = self.gk.check_blacklist(address_upper)
        self.assertIsNotNone(result_upper)
        self.assertEqual(result_upper['address'], "0xBadGuy123")

    def test_check_blacklist_empty(self):
        """Test behavior when blacklist is empty."""
        self.gk.blacklist = []
        address = "0xBadGuy123"
        result = self.gk.check_blacklist(address)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
