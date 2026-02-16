import httpx
import asyncio
import logging

class GoPlusConnector:
    """
    GoPlus Security API Connector.
    Provides real-time security analysis for tokens and contracts.
    """
    def __init__(self):
        self.base_url = "https://api.gopluslabs.io/api/v1"
        self.chain_map = {
            "ETH": "1",
            "ERC20": "1",
            "BSC": "56",
            "BEP20": "56",
            "POLYGON": "137",
            "ARBITRUM": "42161",
            "OPTIMISM": "10",
            "AVALANCHE": "43114"
        }

    async def check_token_security(self, address, network):
        """
        Checks token security metrics (honeypot, blacklist, etc).
        """
        chain_id = self.chain_map.get(network.upper())
        if not chain_id:
            return None, f"Rede {network} não suportada pela análise de segurança GoPlus."

        url = f"{self.base_url}/token_security/{chain_id}"
        params = {"contract_addresses": address}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                if response.status_code != 200:
                    return None, f"Erro GoPlus API: {response.status_code}"
                
                data = response.json()
                if data.get('code') != 1 or not data.get('result'):
                    return None, "Dados de segurança não encontrados para este endereço."

                # O GoPlus retorna um dicionário onde a chave é o endereço do contrato
                result = data['result'].get(address.lower()) or data['result'].get(address)
                if not result:
                    return None, "Resultado vazio para o endereço solicitado."

                return self._parse_security_result(result), None
            except Exception as e:
                return None, f"Falha na consulta GoPlus: {str(e)}"

    def _parse_security_result(self, res):
        """
        Parses raw GoPlus result into a simplified security report.
        """
        return {
            "is_honeypot": res.get("is_honeypot") == "1",
            "is_blacklisted": res.get("is_blacklisted") == "1",
            "is_in_dex": res.get("is_in_dex") == "1",
            "can_take_back_ownership": res.get("can_take_back_ownership") == "1",
            "owner_change_balance": res.get("owner_change_balance") == "1",
            "hidden_owner": res.get("hidden_owner") == "1",
            "self_destruct": res.get("self_destruct") == "1",
            "external_call": res.get("external_call") == "1",
            "trust_score_impact": self._calculate_impact(res)
        }

    def _calculate_impact(self, res):
        """Calculates negative impact on trust score based on flags."""
        impact = 0
        if res.get("is_honeypot") == "1": impact += 80
        if res.get("is_blacklisted") == "1": impact += 40
        if res.get("can_take_back_ownership") == "1": impact += 30
        if res.get("hidden_owner") == "1": impact += 20
        if res.get("self_destruct") == "1": impact += 50
        return impact

if __name__ == "__main__":
    async def test():
        gp = GoPlusConnector()
        # Testando com um endereço conhecido (WETH no ETH)
        res, err = await gp.check_token_security("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", "ETH")
        print(res if res else err)
    
    # asyncio.run(test())
