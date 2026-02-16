import json
import re
import os
from core.connectors.binance_api import BinanceConnector
from core.connectors.cmc_api import CMCConnector
from core.connectors.ccxt_connector import CCXTConnector

class Gatekeeper:
    def __init__(self, registry_path='core/registry/networks.json', blacklist_path='core/registry/blacklist.json'):
        # ... (código anterior mantido) ...
        self.burn_addresses = [
            "0x0000000000000000000000000000000000000000",
            "0x000000000000000000000000000000000000dead",
            "0xdead000000000000000004206942069420694206"
        ]
        # ... (restante do init) ...

    def check_burn_address(self, address):
        """Verifica se o endereço é um destino de queima (irrecuperável)."""
        return address.lower() in self.burn_addresses

    def check_compatibility(self, origin_cex, destination, asset, network, address, on_chain_data=None):
        """
        Versão V5: Detecção de Burn e On-Chain Awareness.
        """
        # --- PRIORIDADE 0: Burn Address (Queima de fundos) ---
        if self.check_burn_address(address):
            return {
                "status": "BURN_ADDRESS_DETECTED",
                "risk": "CRITICAL",
                "message": "Este endereço é um destino de QUEIMA (Burn Address). Enviar fundos para cá resultará na destruição permanente dos tokens."
            }

        # --- PRIORIDADE 1: DEFCON 1 (Blacklist) ---
        incident = self.check_blacklist(address)
        if incident:
            return {
                "status": "BLACK-LISTED",
                "risk": "CRITICAL_DEFCON_1",
                "message": f"ALERTA GOLPE: {incident['description']}",
                "threat_type": incident['threat_type']
            }

        # --- PRIORIDADE 1.5: Smart Contract Awareness ---
        if on_chain_data and on_chain_data.get('is_contract'):
            # Se o usuário acha que é uma Wallet mas é um Contrato
            if destination.lower() not in ["exchange", "contrato", "dapp"]:
                return {
                    "status": "UNEXPECTED_CONTRACT",
                    "risk": "MEDIUM",
                    "message": "O destino é um Smart Contract, não uma carteira pessoal (EOA). Verifique se o contrato aceita este ativo diretamente."
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
        if destination.lower() in ["binance", "okx", "bybit", "gateio"]:
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
