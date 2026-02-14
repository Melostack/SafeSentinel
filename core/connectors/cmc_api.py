import requests
import os
from dotenv import load_dotenv

load_dotenv()

class CMCConnector:
    def __init__(self):
        self.base_url = "https://pro-api.coinmarketcap.com"
        self.api_key = os.getenv("CMC_API_KEY")

    def get_token_metadata(self, symbol):
        """
        Busca metadados do token, incluindo redes suportadas e endereços de contrato.
        """
        if not self.api_key:
            return None, "API Key da CMC não configurada."

        endpoint = "/v2/cryptocurrency/info"
        params = {"symbol": symbol.upper()}
        headers = {
            "X-CMC_PRO_API_KEY": self.api_key,
            "Accept": "application/json"
        }

        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            token_info = data['data'][symbol.upper()][0]
            
            # Extrair plataformas/redes e contratos
            platforms = token_info.get('platforms', [])
            
            result = {
                "name": token_info.get('name'),
                "symbol": token_info.get('symbol'),
                "id": token_info.get('id'),
                "description": token_info.get('description'),
                "networks": platforms # Lista de dicts com {'name': ..., 'address': ...}
            }
            return result, None

        except Exception as e:
            return None, f"Erro ao consultar CMC: {str(e)}"

if __name__ == "__main__":
    cmc = CMCConnector()
    print(f"--- Consultando metadados de USDT na CMC ---")
    info, error = cmc.get_token_metadata("USDT")
    if error:
        print(f"Erro: {error}")
    else:
        print(f"Token: {info['name']} ({info['symbol']})")
        print("Redes e Contratos:")
        for net in info['networks']:
            print(f"- {net['platform']['name']}: {net['contract_address']}")
