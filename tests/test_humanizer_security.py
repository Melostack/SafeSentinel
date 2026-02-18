from core.humanizer import Humanizer
from unittest.mock import MagicMock, patch
import unittest

class TestHumanizerSecurity(unittest.TestCase):
    @patch('core.humanizer.requests.post')
    def test_humanize_risk_headers_fix(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'Risks explained.'
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response

        hm = Humanizer(api_key="fake_key")
        gatekeeper_data = {
            "status": "DANGER",
            "risk": "CRITICAL",
            "message": "Test message"
        }

        # Run method
        result = hm.humanize_risk(gatekeeper_data)

        # Assertions
        self.assertEqual(result, 'Risks explained.')

        # Verify headers were passed
        args, kwargs = mock_post.call_args
        self.assertIn('headers', kwargs)
        self.assertEqual(kwargs['headers'], {'Content-Type': 'application/json'})

        # Verify timeout was added (Security Enhancement)
        self.assertIn('timeout', kwargs)
        self.assertEqual(kwargs['timeout'], 10)

if __name__ == "__main__":
    unittest.main()
