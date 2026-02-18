import unittest
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.gatekeeper import Gatekeeper

class TestGatekeeperData(unittest.TestCase):
    def test_registry_loading(self):
        gk = Gatekeeper()
        self.assertIn("exchanges", gk.registry)
        self.assertIn("wallets", gk.registry)
        self.assertIn("Binance", gk.registry["exchanges"])
        self.assertIn("MetaMask", gk.registry["wallets"])

    def test_blacklist_loading(self):
        gk = Gatekeeper()
        self.assertIsInstance(gk.blacklist, list)

if __name__ == '__main__':
    unittest.main()
