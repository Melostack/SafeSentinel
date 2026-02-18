from core.sourcing_agent import SourcingAgent
from unittest.mock import MagicMock, patch
import unittest

class TestSourcingAgentSecurity(unittest.TestCase):
    @patch('core.sourcing_agent.requests.post')
    def test_find_best_route_timeout(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': '{"steps": [], "cex_source": "Binance", "bridge_needed": false, "recommended_bridge": null, "warning": "None"}'
                }
            }]
        }
        mock_post.return_value = mock_response

        agent = SourcingAgent(api_key="fake_key")

        # Run method
        result, error = agent.find_best_route("USDT", "TRC20")

        # Assertions
        self.assertIsNotNone(result)
        self.assertIsNone(error)

        # Verify timeout was added (Security Enhancement)
        args, kwargs = mock_post.call_args
        self.assertIn('timeout', kwargs)
        self.assertEqual(kwargs['timeout'], 15)

if __name__ == "__main__":
    unittest.main()
