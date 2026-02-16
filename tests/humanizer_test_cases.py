import unittest
import json
from core.humanizer import Humanizer

class TestHumanizerWisdom(unittest.TestCase):
    def setUp(self):
        self.humanizer = Humanizer()
        
    def test_case_binance_to_metamask_mismatch(self):
        """Caso A: USDT de Binance (BEP20) para MetaMask (ERC20-only)."""
        data = {
            "status": "MISMATCH",
            "risk": "CRITICAL",
            "message": "A MetaMask não suporta a rede Tron (TRC20).",
            "asset": "USDT",
            "origin_exchange": "Binance",
            "destination": "MetaMask",
            "selected_network": "TRC20",
            "trust_score": 95
        }
        response = self.humanizer.humanize_risk(data)
        print(f"\n--- Caso A (Mismatch): ---\n{response}")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 50)
        # Verifica se há tom didático/metáfora (esperado no protocolo Nudge)
        
    def test_case_honeypot_risk(self):
        """Caso B: Token com Trust Score baixo (Risco de Honeypot)."""
        data = {
            "status": "SAFE", # Gatekeeper vê rede OK, mas Trust Score é baixo
            "risk": "HIGH",
            "message": "Caminho validado, mas o ativo possui baixa liquidez.",
            "asset": "SHITCOIN",
            "origin_exchange": "MetaMask",
            "destination": "PancakeSwap",
            "selected_network": "BEP20",
            "trust_score": 15
        }
        response = self.humanizer.humanize_risk(data)
        print(f"\n--- Caso B (Honeypot/Low Trust): ---\n{response}")
        self.assertIn("score", response.lower() or "confiança" in response.lower())

    def test_case_contract_warning(self):
        """Caso C: Envio para um Smart Contract em vez de EOA."""
        data = {
            "status": "SAFE",
            "risk": "MEDIUM",
            "message": "Endereço de destino é um Smart Contract.",
            "asset": "ETH",
            "origin_exchange": "Bybit",
            "destination": "Endereço Externo",
            "selected_network": "ERC20",
            "on_chain": {"address_type": "Contract"},
            "trust_score": 100
        }
        response = self.humanizer.humanize_risk(data)
        print(f"\n--- Caso C (Contract): ---\n{response}")
        self.assertTrue("contrato" in response.lower() or "estratégia" in response.lower())

if __name__ == "__main__":
    unittest.main()
