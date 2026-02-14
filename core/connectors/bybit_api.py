import requests
import hashlib
import hmac
import time
import os
from dotenv import load_dotenv

load_dotenv()

class BybitConnector:
    def __init__(self):
        self.base_url = "https://api.bybit.com"
        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")

    def _generate_signature(self, params):
        # Bybit V5 usa uma lógica de assinatura específica
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        param_str = timestamp + self.api_key + recv_window + params
        return hmac.new(self.api_secret.encode('utf-8'), param_str.encode('utf-8'), hashlib.sha256).hexdigest()

    def get_supported_networks(self, asset):
        """
        Consulta a API da Bybit V5 para ver as redes suportadas.
        Endpoint: /v5/asset/coin/query-info
        """
        if not self.api_key or not self.api_secret:
            return None, "API Key ou Secret da Bybit ausente."

        endpoint = "/v5/asset/coin/query-info"
        timestamp = str(int(time.time() * 1000))
        params = f"coin={asset.upper()}"
        
        signature = self._generate_signature(params)
        
        headers = {
            "X-BSRV-APIKEY": self.api_key,
            "X-BSRV-TRANS-TIME": timestamp,
            "X-BSRV-SIGN": signature,
            "X-BSRV-RECV-WINDOW": "5000"
        }

        try:
            response = requests.get(f"{self.base_url}{endpoint}?{params}", headers=headers)
            data = response.json()
            
            if data['retCode'] == 0:
                coin_info = data['result']['rows'][0]
                networks = []
                for net in coin_info['chains']:
                    networks.append({
                        "network": net['chain'],
                        "withdraw_enable": net['chainWithdraw'] == '1',
                        "deposit_enable": net['chainDeposit'] == '1',
                        "name": net['chain']
                    })
                return networks, None
            else:
                return None, f"Erro Bybit: {data['retMsg']}"

        except Exception as e:
            return None, f"Erro ao consultar API da Bybit: {str(e)}"
