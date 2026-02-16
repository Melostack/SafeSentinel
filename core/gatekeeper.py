import json
import re
import os
import base58
from core.connectors.binance_api import BinanceConnector
from core.connectors.cmc_api import CMCConnector
from core.connectors.ccxt_connector import CCXTConnector

class Gatekeeper:
    def __init__(self, registry_path='core/registry/networks.json', blacklist_path='core/registry/blacklist.json'):
        # Carregar Registry Local
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

        self.burn_addresses = [
            "0x0000000000000000000000000000000000000000",
            "0x000000000000000000000000000000000000dead",
            "0xdead000000000000000004206942069420694206"
        ]
        
        self.scam_tokens = ["XRP-SCAM", "FREE-BTC", "MUSK-TOKEN", "TEST-SCAM"]
        
        # Conectores
        self.cmc = CMCConnector()
        self.ccxt_conn = CCXTConnector()

    def check_blacklist(self, address):
        """Retorna detalhes se o endereço estiver na blacklist."""
        for entry in self.blacklist:
            if entry['address'].lower() == address.lower():
                return entry
        return None

    def check_burn_address(self, address):
        """Verifica se o endereço é um destino de queima (irrecuperável)."""
        return address.lower() in self.burn_addresses

    def check_scam_token(self, asset):
        """Bloqueia tokens conhecidos por serem golpes."""
        return asset.upper() in self.scam_tokens

    def validate_address_format(self, address, network):
        """Valida o formato do endereço baseado na rede com precisão criptográfica."""
        net_upper = network.upper()
        
        # 1. Validação EVM (Ethereum, BSC, Polygon, etc)
        evm_nets = ["ERC20", "BEP20", "POLYGON", "ARBITRUM", "OPTIMISM", "BASE", "AVALANCHE"]
        if any(n in net_upper for n in evm_nets) or net_upper == "ETH":
            if re.match(r"^0x[a-fA-F0-9]{40}$", address):
                return True, "Válido (EVM)"
            return False, f"Endereço inválido para rede {network}. Deve começar com 0x e ter 42 caracteres."

        # 2. Validação TRON (Base58Check)
        if net_upper in ["TRC20", "TRX", "TRON"]:
            try:
                decoded = base58.b58decode_check(address)
                if len(decoded) == 21 and decoded[0] == 0x41: # 0x41 = 'T' prefix
                    return True, "Válido (TRON)"
                return False, "Endereço Tron inválido (Checksum ou Prefixo incorreto)."
            except Exception:
                return False, "Endereço Tron inválido (Erro de decodificação Base58)."

        # 3. Validação SOLANA (Base58)
        if net_upper in ["SOL", "SOLANA", "SPL"]:
            try:
                decoded = base58.b58decode(address)
                if len(decoded) == 32:
                    return True, "Válido (SOLANA)"
                return False, f"Endereço Solana inválido (Tamanho incorreto: {len(decoded)} bytes)."
            except Exception:
                return False, "Endereço Solana inválido (Caracteres não-Base58)."

        return True, "Formato não verificado (Rede desconhecida)."

    def check_compatibility(self, origin_cex, destination, asset, network, address, on_chain_data=None, security_audit=None):
        """
        Versão V7: Proteção completa (Scam, Burn, Audit, Format).
        """
        # --- PRIORIDADE -3: Validação de Formato ---
        is_valid_fmt, fmt_msg = self.validate_address_format(address, network)
        if not is_valid_fmt:
            return {
                "status": "INVALID_ADDRESS_FORMAT",
                "risk": "CRITICAL",
                "message": fmt_msg
            }

        # --- PRIORIDADE -2: Security Audit (Malicious Contract Detection) ---
        if security_audit:
            if security_audit.get('is_honeypot'):
                return {
                    "status": "HONEYPOT_DETECTED",
                    "risk": "CRITICAL",
                    "message": f"ALERTA MÁXIMO: O contrato de {asset} é um HONEYPOT. Você conseguirá comprar, mas NUNCA conseguirá vender."
                }
            if security_audit.get('is_blacklisted'):
                return {
                    "status": "ADDRESS_BLACKLISTED",
                    "risk": "CRITICAL",
                    "message": f"ALERTA: Este endereço de {asset} está em uma blacklist de segurança. Os fundos podem ser bloqueados."
                }
            if security_audit.get('trust_score_impact', 0) > 50:
                return {
                    "status": "HIGH_RISK_CONTRACT",
                    "risk": "HIGH",
                    "message": f"Cuidado: O contrato de {asset} possui múltiplas funções de alto risco (ex: autodeclaração de propriedade ou pausa de transferências)."
                }

        # --- PRIORIDADE -1: Scam Tokens ---
        if self.check_scam_token(asset):
            return {
                "status": "SCAM_TOKEN_DETECTED",
                "risk": "CRITICAL",
                "message": f"ALERTA: O ativo {asset} foi identificado como um golpe conhecido ou possui alto risco de segurança."
            }

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
            if destination.lower() not in ["exchange", "contrato", "dapp"]:
                return {
                    "status": "UNEXPECTED_CONTRACT",
                    "risk": "MEDIUM",
                    "message": "O destino é um Smart Contract, não uma carteira pessoal (EOA). Verifique se o contrato aceita este ativo diretamente."
                }

        # --- PRIORIDADE 2: Validação de Origem (CEX) via CCXT ---
        networks, error = self.ccxt_conn.get_supported_networks(origin_cex, asset)
        
        if not error and networks:
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
            pass

        # --- PRIORIDADE 3: Validação de Destino (Wallet/CEX) ---
        if destination == "MetaMask" and network.upper() in ["TRC20", "TRX"]:
            return {
                "status": "MISMATCH", 
                "risk": "CRITICAL", 
                "message": "A MetaMask não suporta a rede Tron (TRC20). O envio resultará em perda total de fundos."
            }

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
