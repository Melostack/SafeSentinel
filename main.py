import os
import asyncio
from core.gatekeeper import Gatekeeper
from core.humanizer import Humanizer

async def run_safe_transfer_check(asset, origin, destination, network, address):
    # 1. Gatekeeper (Lógica Binária)
    gk = Gatekeeper("core/registry/networks.json")
    
    print(f"\n🔍 Analisando: {asset} de {origin} para {destination} via {network}...")
    
    # Validação de Formato
    is_valid_format, format_msg = gk.validate_address_format(address, "EVM")
    if not is_valid_format:
        print(f"❌ Erro de Formato: {format_msg}")
        # Mesmo com erro de formato, o Gatekeeper continua para checar a rede
    
    # Validação de Compatibilidade
    gk_res = gk.check_compatibility(origin, destination, asset, network, address)
    
    # Injetar dados extras para o Humanizer
    gk_res["asset"] = asset
    gk_res["origin_exchange"] = origin
    gk_res["destination"] = destination
    gk_res["selected_network"] = network

    # 2. Humanizer (Inteligência Artificial)
    # Se o status não for SAFE, pedimos para a IA explicar
    if gk_res["status"] != "SAFE" or not is_valid_format:
        hm = Humanizer()
        print("\n--- RESPOSTA DO MENTOR DE SEGURANÇA ---")
        explanation = await hm.humanize_risk(gk_res)
        print(explanation)
    else:
        print("\n✅ TUDO OK: O caminho é seguro e a rede é compatível.")

if __name__ == "__main__":
    # Caso de Sucesso do MVP: Erro de Rede (Binance BEP20 -> MetaMask ERC20)
    # Usando o mesmo cenário que o Arquiteto definiu como Critério de Sucesso.
    asyncio.run(run_safe_transfer_check(
        asset="USDT",
        origin="Binance",
        destination="MetaMask",
        network="BEP20",
        address="0x1234567890123456789012345678901234567890"
    ))
