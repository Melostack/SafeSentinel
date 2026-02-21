import unittest
from unittest.mock import MagicMock, patch
from core.gatekeeper import Gatekeeper

class TestGatekeeper(unittest.TestCase):
    def setUp(self):
        self.gatekeeper = Gatekeeper()
        self.gatekeeper.ccxt_conn = MagicMock()

    def test_destination_check_supported_exchange(self):
        # Mocking get_supported_networks to return a valid network for the destination
        self.gatekeeper.ccxt_conn.get_supported_networks.side_effect = [
            # First call for origin_cex (SAFE)
            ([{'network': 'TRC20', 'withdraw_enable': True}], None),
            # Second call for destination (Binance)
            ([{'network': 'TRC20', 'deposit_enable': True}], None)
        ]

        result = self.gatekeeper.check_compatibility(
            origin_cex="SomeOrigin",
            destination="Binance", # In the hardcoded list
            asset="USDT",
            network="TRC20",
            address="TAddress123"
        )

        # It should have called get_supported_networks for the destination
        self.assertEqual(self.gatekeeper.ccxt_conn.get_supported_networks.call_count, 2)
        # Verify the second call was for the destination
        self.gatekeeper.ccxt_conn.get_supported_networks.assert_called_with("Binance", "USDT")

        self.assertEqual(result['status'], "SAFE")

    def test_destination_check_unsupported_exchange(self):
        # Mocking get_supported_networks just for origin
        self.gatekeeper.ccxt_conn.get_supported_networks.return_value = (
             [{'network': 'TRC20', 'withdraw_enable': True}], None
        )

        result = self.gatekeeper.check_compatibility(
            origin_cex="SomeOrigin",
            destination="UnknownExchange", # NOT in the hardcoded list
            asset="USDT",
            network="TRC20",
            address="TAddress123"
        )

        # It should ONLY call get_supported_networks for the origin, NOT for the destination
        self.assertEqual(self.gatekeeper.ccxt_conn.get_supported_networks.call_count, 1)
        self.gatekeeper.ccxt_conn.get_supported_networks.assert_called_with("SomeOrigin", "USDT")

        self.assertEqual(result['status'], "SAFE")

    def test_destination_check_case_insensitive(self):
        # Mocking get_supported_networks to return a valid network for the destination
        self.gatekeeper.ccxt_conn.get_supported_networks.side_effect = [
            # First call for origin_cex (SAFE)
            ([{'network': 'TRC20', 'withdraw_enable': True}], None),
            # Second call for destination (Okx)
            ([{'network': 'TRC20', 'deposit_enable': True}], None)
        ]

        result = self.gatekeeper.check_compatibility(
            origin_cex="SomeOrigin",
            destination="Okx", # In the list (case insensitive check)
            asset="USDT",
            network="TRC20",
            address="TAddress123"
        )

        # It should have called get_supported_networks for the destination
        self.assertEqual(self.gatekeeper.ccxt_conn.get_supported_networks.call_count, 2)

        self.assertEqual(result['status'], "SAFE")

if __name__ == '__main__':
    unittest.main()
