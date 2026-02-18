import json
import re
import os
from core.connectors.binance_api import BinanceConnector
from core.connectors.cmc_api import CMCConnector
from core.connectors.ccxt_connector import CCXTConnector

class Gatekeeper:
    SUPPORTED_CEX_DESTINATIONS = ["binance", "okx", "bybit", "gateio"]

    def __init__(self, registry_path='core/registry/networks.json', blacklist_path='core/registry/blacklist.json'):
        # Carregar Registry Local (Para Wallets e regras fixas)
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
        
        # Conectores
        self.cmc = CMCConnector()
        self.ccxt_conn = CCXTConnector()

    def check_blacklist(self, address):
        """Retorna detalhes se o endereço estiver na blacklist."""
        for entry in self.blacklist:
            if entry['address'].lower() == address.lower():
                return entry
        return None

    def validate_address_format(self, address, network):
        """Valida o formato do endereço baseado na rede."""
        net_upper = network.upper()
        type_map = {
            "ERC20": "EVM", "BEP20": "EVM", "POLYGON": "EVM", "ARBITRUM": "EVM", "OPTIMISM": "EVM",
            "TRC20": "TRON", "TRX": "TRON",
            "SOL": "SOLANA", "SOLANA": "SOLANA"
        }
        addr_type = type_map.get(net_upper, "EVM")
        pattern = self.patterns.get(addr_type)
        if not pattern: return True, "Formato não verificado."
        return (True, "Válido") if re.match(pattern, address) else (False, f"O formato do endereço é inválido para a rede {network}.")

    def check_compatibility(self, origin_cex, destination, asset, network, address):
        """
        Versão V4: Onisciência de Exchanges via CCXT.
        """
        # --- PRIORIDADE 1: DEFCON 1 (Blacklist) ---
        incident = self.check_blacklist(address)
        if incident:
            return {
                "status": "BLACK-LISTED",
                "risk": "CRITICAL_DEFCON_1",
                "message": f"ALERTA GOLPE: {incident['description']}",
                "threat_type": incident['threat_type']
            }

        # --- PRIORIDADE 2: Validação de Origem (CEX) via CCXT ---
        # Aceita 'Binance', 'OKX', 'Bybit', 'KuCoin', etc.
        networks, error = self.ccxt_conn.get_supported_networks(origin_cex, asset)
        
        if not error and networks:
            # Tentar encontrar a rede (considerando a normalização do CCXTConnector)
            # O front manda 'BEP20', o conector normaliza 'BSC' para 'BEP20'.
            match = next((n for n in networks if n['network'].upper() == network.upper()), None)
            
            if not match:
                return {
                    "status": "UNSUPPORTED_ON_ORIGIN", 
                    "risk": "HIGH", 
                    "message": f"A exchange {origin_cex} não suporta saques de {asset} via rede {network}."
                }
            
            if not match['withdraw_enable']:
                return {
                    "status": "WITHDRAW_DISABLED", 
                    "risk": "HIGH", 
                    "message": f"Saques de {asset} via {network} estão suspensos ou em manutenção na {origin_cex}."
                }
        elif error:
            # Se a exchange não for suportada pela CCXT, o Humanizer usará SafeDiscovery (Intel Search)
            pass

        # --- PRIORIDADE 3: Validação de Destino (Wallet/CEX) ---
        # Lógica de Mismatch conhecida (MetaMask vs Tron)
        if destination == "MetaMask" and network.upper() in ["TRC20", "TRX"]:
            return {
                "status": "MISMATCH", 
                "risk": "CRITICAL", 
                "message": "A MetaMask não suporta a rede Tron (TRC20). O envio resultará em perda total de fundos."
            }

        # Caso o destino também seja uma CEX (Transferência entre Corretoras)
        if destination.lower() in self.SUPPORTED_CEX_DESTINATIONS:
            dest_networks, dest_error = self.ccxt_conn.get_supported_networks(destination, asset)
            if not dest_error and dest_networks:
                dest_match = next((n for n in dest_networks if n['network'].upper() == network.upper()), None)
                if not dest_match or not dest_match['deposit_enable']:
                    return {
                        "status": "DEPOSIT_DISABLED_AT_DESTINATION",
                        "risk": "CRITICAL",
                        "message": f"O destino ({destination}) NÃO aceita depósitos de {asset} via {network}. Se você enviar, os fundos não serão creditados."
                    }

        return {"status": "SAFE", "risk": "LOW", "message": "Caminho validado e compatível."}
