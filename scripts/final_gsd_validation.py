import sys
import os
import asyncio
import json

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.gatekeeper import Gatekeeper
from core.humanizer import Humanizer

async def simulate_scenario(name, origin, destination, asset, network, address):
    print(f"\n--- SIMULANDO: {name} ---")
    gk = Gatekeeper()
    hm = Humanizer()
    
    # 1. Validação do Gatekeeper
    gk_res = gk.check_compatibility(origin, destination, asset, network, address)
    print(f"Status do Gatekeeper: {gk_res['status']} | Risco: {gk_res['risk']}")
    
    # 2. Humanização pela MarIA
    if gk_res['status'] != 'SAFE':
        explanation = hm.humanize_risk(gk_res)
        print(f"MarIA explica: {explanation}")
    else:
        print(f"MarIA aprova: {gk_res['message']}")

async def main():
    # Cenário 1: O clássico erro de rede (Tron -> MetaMask)
    await simulate_scenario(
        "Risco Crítico (Tron -> MetaMask)",
        origin="Binance",
        destination="MetaMask",
        asset="USDT",
        network="TRC20",
        address="0x1234567890123456789012345678901234567890"
    )

    # Cenário 2: Brasil Context (Mercado Bitcoin -> MetaMask)
    await simulate_scenario(
        "Brasil: Mercado Bitcoin -> MetaMask (Seguro)",
        origin="Mercado Bitcoin",
        destination="MetaMask",
        asset="ETH",
        network="ERC20",
        address="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )

    # Cenário 3: Novo bloqueio Solana
    await simulate_scenario(
        "Risco Crítico (Solana -> MetaMask)",
        origin="Binance",
        destination="MetaMask",
        asset="SOL",
        network="SOL",
        address="0x12345"
    )

if __name__ == "__main__":
    asyncio.run(main())
