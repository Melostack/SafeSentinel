import ccxt
import logging

class CCXTConnector:
    def __init__(self):
        self.exchanges = {}
        # Mapeamento para normalizar nomes de redes vindos de diferentes corretoras
        self.network_map = {
            "BSC": "BEP20",
            "BNB Smart Chain (BEP20)": "BEP20",
            "ETH": "ERC20",
            "Ethereum (ERC20)": "ERC20",
            "TRX": "TRC20",
            "Tron (TRC20)": "TRC20",
            "AVAXC": "AVAX-C",
            "MATIC": "Polygon"
        }

    def _normalize_network(self, net_name):
        """Normaliza o nome da rede para o padrão do SafeSentinel."""
        return self.network_map.get(net_name, net_name)

    def get_exchange_instance(self, exchange_id):
        exchange_id = exchange_id.lower()
        if exchange_id not in self.exchanges:
            try:
                exchange_class = getattr(ccxt, exchange_id)
                self.exchanges[exchange_id] = exchange_class({
                    'timeout': 20000,
                    'enableRateLimit': True,
                })
            except Exception:
                return None
        return self.exchanges[exchange_id]

    def get_supported_networks(self, exchange_id, asset):
        """
        Versão Profissional: Consulta metadados de moedas e redes via CCXT.
        Prioriza fetch_currencies() para dados mais precisos de saque/depósito.
        """
        exchange = self.get_exchange_instance(exchange_id)
        if not exchange:
            return None, f"Exchange '{exchange_id}' não suportada."

        try:
            # 1. Carregar mercados (base para tudo)
            exchange.load_markets()
            
            currencies = {}
            # 2. Tentar obter dados detalhados de moedas se a exchange suportar
            if exchange.has.get('fetchCurrencies'):
                currencies = exchange.fetch_currencies()
            else:
                currencies = exchange.currencies

            if asset.upper() in currencies:
                coin_data = currencies[asset.upper()]
                # A CCXT padroniza redes no campo 'networks' (se disponível)
                raw_networks = coin_data.get('networks', {})
                
                if not raw_networks:
                    # Algumas exchanges colocam info de saque no nível raiz da moeda
                    return [{
                        "network": self._normalize_network(asset.upper()),
                        "withdraw_enable": coin_data.get('withdraw', True),
                        "deposit_enable": coin_data.get('deposit', True),
                        "name": coin_data.get('name', asset.upper())
                    }], None

                res = []
                for net_id, net_info in raw_networks.items():
                    # Extrair o nome legível se existir, senão usa o ID técnico
                    display_name = net_info.get('name', net_id)
                    res.append({
                        "network": self._normalize_network(net_id),
                        "withdraw_enable": net_info.get('withdraw', net_info.get('active', True)),
                        "deposit_enable": net_info.get('deposit', net_info.get('active', True)),
                        "name": display_name
                    })
                return res, None
            
            return None, f"Ativo '{asset}' não localizado na {exchange_id} via API."

        except Exception as e:
            logging.error(f"CCXT Error: {str(e)}")
            return None, f"Erro de conexão com a exchange {exchange_id}."

if __name__ == "__main__":
    conn = CCXTConnector()
    # Teste com OKX (uma das mais complexas em termos de redes)
    print(f"--- Consultando OKX: USDT ---")
    networks, err = conn.get_supported_networks("okx", "USDT")
    if err:
        print(f"Erro: {err}")
    else:
        for n in networks:
            print(f"- Rede: {n['network']} | Saque Ativo: {n['withdraw_enable']} | Nome: {n['name']}")
