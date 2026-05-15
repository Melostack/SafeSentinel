import unittest
import urllib.parse
from core.connectors.binance_api import BinanceConnector
from core.connectors.bybit_api import BybitConnector
import os
from unittest.mock import patch, MagicMock

class TestConnectors(unittest.TestCase):
    @patch('os.getenv')
    def test_binance_signature(self, mock_getenv):
        mock_getenv.side_effect = lambda key: "secret" if key == "BINANCE_API_SECRET" else "key"
        conn = BinanceConnector()
        params = {"timestamp": 123, "asset": "USDT&attack=1"}
        sig = conn._generate_signature(params)
        self.assertIsNotNone(sig)

    @patch('os.getenv')
    def test_bybit_signature(self, mock_getenv):
        mock_getenv.side_effect = lambda key: "secret" if key == "BYBIT_API_SECRET" else "key"
        conn = BybitConnector()
        timestamp = "12345"
        params_dict = {"coin": "USDT&attack=1"}
        payload_str = urllib.parse.urlencode(params_dict)
        sig = conn._generate_signature(timestamp, payload_str)
        self.assertIsNotNone(sig)

if __name__ == '__main__':
    unittest.main()
