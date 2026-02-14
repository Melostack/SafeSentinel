import ccxt
import logging

class CCXTConnector:
    def __init__(self):
        self.exchanges = {}

    def get_exchange_instance(self, exchange_id):
        exchange_id = exchange_id.lower()
        if exchange_id not in self.exchanges:
            try:
                exchange_class = getattr(ccxt, exchange_id)
                self.exchanges[exchange_id] = exchange_class()
            except Exception:
                return None
        return self.exchanges[exchange_id]

    def get_supported_networks(self, exchange_id, asset):
        """
        Consulta a CCXT para ver as redes suportadas pela exchange para um ativo.
        """
        exchange = self.get_exchange_instance(exchange_id)
        if not exchange:
            return None, f"Exchange '{exchange_id}' não suportada pela CCXT."

        try:
            # Algumas exchanges exigem carregar os mercados primeiro
            exchange.load_markets()
            
            # Tentar buscar informações da moeda (moedas costumam ter o campo 'networks')
            if hasattr(exchange, 'currencies') and asset.upper() in exchange.currencies:
                currency = exchange.currencies[asset.upper()]
                networks = currency.get('networks', {})
                
                if not networks:
                    # Fallback: algumas APIs não listam redes no currencies, 
                    # mas podem ter em fetchCurrencies se disponível
                    return None, "Redes não listadas diretamente. Iniciando busca via SafeDiscovery."
                
                res = []
                for net_id, net_info in networks.items():
                    res.append({
                        "network": net_id,
                        "withdraw_enable": net_info.get('withdraw', True),
                        "deposit_enable": net_info.get('deposit', True),
                        "name": net_info.get('name', net_id)
                    })
                return res, None
            
            return None, f"Ativo '{asset}' não encontrado na {exchange_id}."

        except Exception as e:
            return None, f"Erro na CCXT ({exchange_id}): {str(e)}"

if __name__ == "__main__":
    conn = CCXTConnector()
    print(f"--- Testando CCXT: OKX + USDT ---")
    networks, err = conn.get_supported_networks("okx", "USDT")
    if err:
        print(f"Erro: {err}")
    else:
        for n in networks:
            print(f"- {n['network']}: Saque={n['withdraw_enable']}")
