import unittest
from unittest.mock import patch, MagicMock
from core.connectors.ccxt_connector import CCXTConnector
import sys

# Ensure core is importable
sys.path.append('.')

class TestCCXTConnectorSecurity(unittest.TestCase):
    def setUp(self):
        self.connector = CCXTConnector()

    @patch('core.connectors.ccxt_connector.ccxt')
    def test_vulnerability_demonstration(self, mock_ccxt):
        """
        Demonstrate that the connector attempts to instantiate an arbitrary attribute
        if passed as an exchange ID.
        """
        # Setup mock: 'malicious_attr' is NOT in 'exchanges' but IS an attribute
        mock_ccxt.exchanges = ['binance']
        mock_malicious_class = MagicMock()
        mock_ccxt.malicious_attr = mock_malicious_class

        # Call with the malicious attribute name
        # In vulnerable code, this will instantiate 'malicious_attr'
        self.connector.get_exchange_instance('malicious_attr')

        # Verify that it was NOT called (instantiated) after fix
        self.assertFalse(mock_malicious_class.called, "Should not instantiate arbitrary attribute")

    @patch('core.connectors.ccxt_connector.ccxt')
    def test_security_fix_verification(self, mock_ccxt):
        """
        Verify that after the fix, passing a non-exchange ID (even if it's an attribute)
        does NOT trigger instantiation.
        """
        mock_ccxt.exchanges = ['binance']
        mock_malicious_class = MagicMock()
        mock_ccxt.malicious_attr = mock_malicious_class

        # Also need a valid exchange for comparison
        mock_binance_class = MagicMock()
        mock_ccxt.binance = mock_binance_class

        # 1. Try malicious attribute - should be rejected
        result = self.connector.get_exchange_instance('malicious_attr')
        self.assertIsNone(result, "Result should be None for invalid exchange ID")
        mock_malicious_class.assert_not_called()

        # 2. Try valid exchange - should be accepted
        # We need to ensure 'binance' is in exchanges list and attribute exists
        # mock_ccxt.exchanges already set above

        result_valid = self.connector.get_exchange_instance('binance')
        self.assertIsNotNone(result_valid, "Result should not be None for valid exchange ID")
        mock_binance_class.assert_called_once()

if __name__ == '__main__':
    unittest.main()
