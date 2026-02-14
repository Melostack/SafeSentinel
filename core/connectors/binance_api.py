import requests
import hashlib
import hmac
import time
import os
from dotenv import load_dotenv

load_dotenv()

class BinanceConnector:
    def __init__(self):
        self.base_url = "https://api.binance.com"
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET") # Note: Precisaremos dela para HMAC

    def _generate_signature(self, params):
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def get_supported_networks(self, asset):
        """
        Consulta a API da Binance para ver quais redes suportam depósitos/saques para o ativo.
        """
        if not self.api_key or not self.api_secret:
            return None, "API Key ou Secret da Binance ausente."

        endpoint = "/sapi/v1/capital/config/getall"
        timestamp = int(time.time() * 1000)
        params = {"timestamp": timestamp}
        signature = self._generate_signature(params)
        params["signature"] = signature

        headers = {"X-MBX-APIKEY": self.api_key}

        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Procurar o ativo na lista
            for coin in data:
                if coin['coin'] == asset.upper():
                    networks = []
                    for net in coin['networkList']:
                        networks.append({
                            "network": net['network'],
                            "is_default": net['isDefault'],
                            "withdraw_enable": net['withdrawEnable'],
                            "deposit_enable": net['depositEnable'],
                            "name": net['name']
                        })
                    return networks, None
            
            return None, f"Ativo {asset} não encontrado na Binance."

        except Exception as e:
            return None, f"Erro ao consultar API da Binance: {str(e)}"

if __name__ == "__main__":
    # Teste rápido do conector
    conn = BinanceConnector()
    print(f"--- Consultando redes para USDT na Binance ---")
    networks, error = conn.get_supported_networks("USDT")
    if error:
        print(f"Erro: {error}")
    else:
        for n in networks:
            print(f"- {n['network']} ({n['name']}): Saque={n['withdraw_enable']}")
