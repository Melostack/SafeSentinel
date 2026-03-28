import unittest
from core.connectors.binance_api import BinanceConnector

class TestBinanceConnector(unittest.TestCase):
    def test_generate_signature(self):
        connector = BinanceConnector()
        connector.api_secret = "test_secret"

        # Test basic signature generation
        params = {"timestamp": 1234567890}
        signature = connector._generate_signature(params)
        self.assertTrue(isinstance(signature, str))
        self.assertEqual(len(signature), 64) # SHA256 length

        # Test signature changes with different params
        params2 = {"timestamp": 1234567890, "foo": "bar"}
        signature2 = connector._generate_signature(params2)
        self.assertNotEqual(signature, signature2)

        # Test with potentially injected parameters
        params_injected = {"timestamp": "1234567890&foo=bar"}
        signature_injected = connector._generate_signature(params_injected)
        self.assertNotEqual(signature2, signature_injected)

if __name__ == '__main__':
    unittest.main()
