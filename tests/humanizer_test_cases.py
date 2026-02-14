import sys
import os
import json
import asyncio
from dotenv import load_dotenv

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.getcwd())

from core.humanizer import Humanizer

load_dotenv()

async def run_tests():
    hm = Humanizer()
    print("Iniciando Testes do Humanizer (Sprint 2)\n")

    test_cases = [
        {
            "name": "Caso A: Mismatch de Rede (Binance USDT -> MetaMask Polygon)",
            "data": {
                "status": "UNSUPPORTED_ON_ORIGIN",
                "risk": "HIGH",
                "message": "A exchange Binance não suporta saques de USDT via rede Polygon (Simulado).",
                "asset": "USDT",
                "origin_exchange": "Binance",
                "destination": "MetaMask",
                "selected_network": "Polygon",
                "trust_score": 98,
                "volume_24h": 50000000000,
                "on_chain": {"address_type": "EOA", "label": "Carteira Pessoal"}
            }
        },
        {
            "name": "Caso B: Envio para Contrato de Token (Possível Erro)",
            "data": {
                "status": "SAFE",
                "risk": "LOW",
                "message": "Caminho validado.",
                "asset": "LINK",
                "origin_exchange": "Bybit",
                "destination": "Desconhecido",
                "selected_network": "ERC20",
                "trust_score": 85,
                "volume_24h": 250000000,
                "on_chain": {"address_type": "CONTRACT", "label": "Chainlink Token Contract"}
            }
        },
        {
            "name": "Caso C: Token de Baixa Confiança (Scam)",
            "data": {
                "status": "SAFE",
                "risk": "LOW",
                "message": "Caminho validado.",
                "asset": "SCAM-TOKEN",
                "origin_exchange": "OKX",
                "destination": "MetaMask",
                "selected_network": "BEP20",
                "trust_score": 15,
                "volume_24h": 1200,
                "on_chain": {"address_type": "EOA", "label": "Carteira Pessoal"}
            }
        }
    ]

    for case in test_cases:
        print(f"--- {case['name']} ---")
        response = hm.humanize_risk(case['data'])
        print(f"RESPOSTA:\n{response}\n")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(run_tests())
