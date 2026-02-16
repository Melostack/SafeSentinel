import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

class TransactionSimulator:
    """
    Transaction Simulator: Pre-flight checks using Alchemy Simulation.
    Answers the question: "What happens if I sign this?"
    """
    def __init__(self):
        self.api_key = os.getenv("ALCHEMY_API_KEY")
        # Base URLs por rede para simulação
        self.rpc_urls = {
            "ETH": f"https://eth-mainnet.g.alchemy.com/v2/{self.api_key}",
            "POLYGON": f"https://polygon-mainnet.g.alchemy.com/v2/{self.api_key}",
            "ARBITRUM": f"https://arb-mainnet.g.alchemy.com/v2/{self.api_key}"
        }

    async def simulate_transfer(self, from_addr, to_address, asset, network, value="0x0"):
        """
        Simula uma transferência básica para ver mudanças de saldo e erros.
        """
        if not self.api_key:
            return None, "Alchemy API Key não configurada."

        url = self.rpc_urls.get(network.upper())
        if not url:
            return None, f"Simulação não suportada para a rede {network}."

        # Payload para Alchemy Simulation (alchemy_simulateAssetChanges)
        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "alchemy_simulateAssetChanges",
            "params": [{
                "from": from_addr,
                "to": to_address,
                "value": value
            }]
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=20.0)
                data = response.json()
                
                if "error" in data:
                    return {"status": "REVERTED", "error": data['error'].get('message')}, None
                
                return self._parse_simulation(data.get('result', {})), None
            except Exception as e:
                return None, f"Falha na simulação: {str(e)}"

    def _parse_simulation(self, result):
        """Traduz o resultado da Alchemy em algo legível."""
        changes = result.get('changes', [])
        summary = []
        
        for change in changes:
            change_type = change.get('changeType') # TRANSFER, APPROVAL, etc
            asset = change.get('symbol', 'Unknown')
            amount = change.get('amount', '0')
            
            if change_type == "TRANSFER":
                from_c = change.get('from')
                to_c = change.get('to')
                summary.append({
                    "asset": asset,
                    "amount": amount,
                    "from": from_c,
                    "to": to_c
                })

        return {
            "status": "SUCCESS",
            "changes": summary,
            "gas_used": result.get('gasUsed')
        }

if __name__ == "__main__":
    # Teste rápido (Mock)
    # simulator = TransactionSimulator()
    # print(simulator.simulate_transfer("0x...", "0x...", "USDT", "ETH"))
    pass
