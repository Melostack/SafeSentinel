import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add project root to path so we can import core.humanizer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.humanizer import Humanizer

class TestHumanizer(unittest.TestCase):
    def setUp(self):
        # We need to set an API key to bypass the 'if not self.api_key: return None' check
        self.humanizer = Humanizer(api_key="test_key")

    @patch('requests.post')
    def test_extract_intent_success(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': '```json\n{"asset": "USDT", "network": "ERC20"}\n```'
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response

        # Need to patch requests inside the module or use patch as context manager if import is direct
        # Since we patched requests.post, it should work for imports inside methods too if they use requests.post

        result = self.humanizer.extract_intent("Transfer USDT via ERC20")
        self.assertEqual(result, {"asset": "USDT", "network": "ERC20"})

    @patch('requests.post')
    def test_extract_intent_failure(self, mock_post):
        # Mock exception
        mock_post.side_effect = Exception("API Error")

        result = self.humanizer.extract_intent("Transfer USDT")
        self.assertIsNone(result)

    @patch('requests.post')
    def test_humanize_risk_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'Risk analysis result'
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response

        result = self.humanizer.humanize_risk({'risk': 'LOW', 'message': 'Safe'})
        self.assertEqual(result, 'Risk analysis result')

    @patch('requests.post')
    def test_humanize_risk_failure(self, mock_post):
        mock_post.side_effect = Exception("API Error")

        result = self.humanizer.humanize_risk({'risk': 'LOW', 'message': 'Safe'})
        self.assertEqual(result, "❌ Falha crítica na interpretação de risco.")

if __name__ == '__main__':
    unittest.main()
