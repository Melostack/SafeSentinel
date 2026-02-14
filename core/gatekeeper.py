import json
import re
import os
from connectors.binance_api import BinanceConnector
from connectors.cmc_api import CMCConnector

class Gatekeeper:
    def __init__(self, registry_path='core/registry/networks.json', blacklist_path='core/registry/blacklist.json'):
        if os.path.exists(registry_path):
            with open(registry_path, 'r') as f:
                self.registry = json.load(f)
        else:
            self.registry = {"wallets": {}, "exchanges": {}}
        
        # Carregar Blacklist
        if os.path.exists(blacklist_path):
            with open(blacklist_path, 'r') as f:
                self.blacklist = json.load(f)
        else:
            self.blacklist = []

        self.patterns = {
            "EVM": r"^0x[a-fA-F0-9]{40}$",
            "TRON": r"^T[a-zA-Z0-9]{33}$",
            "SOLANA": r"^[1-9A-HJ-NP-Za-km-z]{32,44}$"
        }
        self.binance = BinanceConnector()
        self.cmc = CMCConnector()

    def check_blacklist(self, address):
        """
        Retorna detalhes se o endereço estiver na blacklist.
        """
        for entry in self.blacklist:
            if entry['address'].lower() == address.lower():
                return entry
        return None

    def validate_address_format(self, address, network):
        net_upper = network.upper()
        type_map = {
            "ERC20": "EVM", "BEP20": "EVM", "POLYGON": "EVM", "ARBITRUM": "EVM", "OPTIMISM": "EVM",
            "TRC20": "TRON", "TRX": "TRON",
            "SOL": "SOLANA", "SOLANA": "SOLANA"
        }
        addr_type = type_map.get(net_upper, "EVM")
        pattern = self.patterns.get(addr_type)
        if not pattern: return True, "Formato não verificado."
        return (True, "Válido") if re.match(pattern, address) else (False, f"Inválido para {network}")

    def check_compatibility(self, origin_cex, destination, asset, network, address):
        # --- PRIORIDADE MÁXIMA: DEFCON 1 ---
        incident = self.check_blacklist(address)
        if incident:
            return {
                "status": "BLACK-LISTED",
                "risk": "CRITICAL_DEFCON_1",
                "message": f"ALERTA GOLPE: {incident['description']}",
                "threat_type": incident['threat_type']
            }

        # 1. Validar Origem via API (Binance)
        if origin_cex.lower() == "binance":
            networks, error = self.binance.get_supported_networks(asset)
            if not error:
                net_map = {"BEP20": "BSC", "ERC20": "ETH", "TRC20": "TRX"}
                search_net = net_map.get(network.upper(), network.upper())
                match = next((n for n in networks if n['network'] == search_net), None)
                
                if not match:
                    return {"status": "UNSUPPORTED_ON_ORIGIN", "risk": "HIGH", "message": f"A {origin_cex} não suporta {asset} via {network}."}
                if not match['withdraw_enable']:
                    return {"status": "WITHDRAW_DISABLED", "risk": "HIGH", "message": f"Saques de {asset} suspensos na {origin_cex}."}

        # 2. Lógica de Mismatch conhecida
        if destination == "MetaMask" and network.upper() in ["TRC20", "TRX"]:
            return {"status": "MISMATCH", "risk": "CRITICAL", "message": "A MetaMask não suporta a rede Tron (TRC20). Você perderá seus fundos."}

        return {"status": "SAFE", "risk": "LOW", "message": "Validação concluída."}
