import unittest
import sys
import os

# Create mock FastAPI and dependencies since they're not installed
class MockFastAPI:
    def add_middleware(self, *args, **kwargs):
        pass
    def get(self, *args, **kwargs):
        return lambda f: f
    def post(self, *args, **kwargs):
        return lambda f: f

class MockHTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail

class MockBaseModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

# Inject mocks into sys.modules
import sys
from unittest.mock import MagicMock, patch

sys.modules['fastapi'] = MagicMock(FastAPI=MockFastAPI, HTTPException=MockHTTPException)
sys.modules['fastapi.middleware.cors'] = MagicMock()
sys.modules['pydantic'] = MagicMock(BaseModel=MockBaseModel)
sys.modules['core'] = MagicMock()
sys.modules['core.gatekeeper'] = MagicMock()
sys.modules['core.humanizer'] = MagicMock()
sys.modules['core.sourcing_agent'] = MagicMock()
sys.modules['core.connectors'] = MagicMock()
sys.modules['core.connectors.web3_rpc_connector'] = MagicMock()

# Now import the server code
from api.server import check_transfer, CheckRequest, app, logger

class TestServerExceptionHandling(unittest.IsolatedAsyncioTestCase):
    async def test_error_handling(self):
        req = CheckRequest(
            asset="USDT",
            origin="Binance",
            destination="Bybit",
            network="TRX",
            address="Txxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        )

        with patch('api.server.OnChainVerifier') as mock_verifier:
            mock_instance = mock_verifier.return_value
            # Trigger exception
            mock_instance.verify_address.side_effect = Exception("Sensitive DB credentials exposed")

            with patch('api.server.logger') as mock_logger:
                with self.assertRaises(MockHTTPException) as context:
                    await check_transfer(req)

                # Verify that exception does NOT contain the sensitive info
                self.assertEqual(context.exception.status_code, 500)
                self.assertEqual(context.exception.detail, "Erro interno do servidor")

                # Verify that logger WAS called to log the actual error
                mock_logger.error.assert_called_once()
                args, kwargs = mock_logger.error.call_args
                self.assertEqual(args[0], "Erro interno no servidor")
                self.assertEqual(kwargs.get("exc_info"), True)

if __name__ == '__main__':
    unittest.main()
