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
        Busca metadados e mercado do token via CMC.
        """
        if not self.api_key:
            return None, "API Key da CMC não configurada."

        headers = {
            "X-CMC_PRO_API_KEY": self.api_key,
            "Accept": "application/json"
        }

        try:
            # 1. Buscar Info (Metadados e Contratos)
            info_url = f"{self.base_url}/v2/cryptocurrency/info"
            info_res = requests.get(info_url, params={"symbol": symbol.upper()}, headers=headers)
            info_res.raise_for_status()
            info_data = info_res.json()['data'][symbol.upper()][0]

            # 2. Buscar Quotes (Preço e Volume)
            quotes_url = f"{self.base_url}/v1/cryptocurrency/quotes/latest"
            quotes_res = requests.get(quotes_url, params={"symbol": symbol.upper()}, headers=headers)
            quotes_res.raise_for_status()
            quote_data = quotes_res.json()['data'][symbol.upper()]

            usd_quote = quote_data['quote']['USD']
            
            result = {
                "name": info_data.get('name'),
                "symbol": info_data.get('symbol'),
                "cmc_id": info_data.get('id'),
                "description": info_data.get('description'),
                "logo": info_data.get('logo'),
                "date_added": quote_data.get('date_added'),
                "max_supply": quote_data.get('max_supply'),
                "circulating_supply": quote_data.get('circulating_supply'),
                "volume_24h": usd_quote.get('volume_24h'),
                "volume_change_24h": usd_quote.get('volume_change_24h'),
                "market_cap": usd_quote.get('market_cap'),
                "contracts": info_data.get('platforms', []),
                "official_links": info_data.get('urls', {})
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
