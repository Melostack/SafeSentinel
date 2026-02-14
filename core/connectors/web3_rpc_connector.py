from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

class Web3RPCConnector:
    def __init__(self):
        # Mapeamento de Redes para RPCs
        self.networks = {
            "ETH": os.getenv("RPC_ETH_MAINNET", "https://eth.llamarpc.com"),
            "BSC": os.getenv("RPC_BSC_MAINNET", "https://binance.llamarpc.com"),
            "POLYGON": os.getenv("RPC_POLYGON", "https://polygon.llamarpc.com"),
            "ARBITRUM": os.getenv("RPC_ARBITRUM", "https://arbitrum.llamarpc.com")
        }
        self.connections = {}

    def get_connection(self, network_key):
        """Retorna uma instância Web3 conectada à rede especificada."""
        if network_key not in self.networks:
            return None
        
        if network_key not in self.connections:
            self.connections[network_key] = Web3(Web3.HTTPProvider(self.networks[network_key]))
        
        return self.connections[network_key]

    def is_contract(self, address, network_key="ETH"):
        """
        Verifica se o endereço é um Contrato Inteligente ou uma Carteira Pessoal (EOA).
        Retorna: True (Contrato), False (EOA), None (Erro/Rede inválida)
        """
        w3 = self.get_connection(network_key)
        if not w3 or not w3.is_connected():
            return None, "Falha na conexão RPC."

        try:
            # Checksum address para garantir validade
            checksum_addr = w3.to_checksum_address(address)
            
            # Pega o código no endereço
            code = w3.eth.get_code(checksum_addr)
            
            # Se o código for '0x', é uma conta externa (EOA). Se tiver hex, é contrato.
            return (code != b''), None
        except Exception as e:
            return None, f"Erro RPC: {str(e)}"

    def get_native_balance(self, address, network_key="ETH"):
        """Retorna o saldo nativo (Gas) do endereço."""
        w3 = self.get_connection(network_key)
        if not w3: return None
        
        try:
            checksum_addr = w3.to_checksum_address(address)
            balance_wei = w3.eth.get_balance(checksum_addr)
            return w3.from_wei(balance_wei, 'ether')
        except: return 0

if __name__ == "__main__":
    # Teste Rápido
    rpc = Web3RPCConnector()
    
    # Endereço de Contrato USDT (ETH)
    usdt_contract = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    is_contract, err = rpc.is_contract(usdt_contract, "ETH")
    print(f"USDT Address is Contract? {is_contract} (Erro: {err})")
    
    # Endereço Aleatório (Provável EOA)
    random_wallet = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    is_contract, err = rpc.is_contract(random_wallet, "ETH")
    print(f"Random Address is Contract? {is_contract} (Erro: {err})")
