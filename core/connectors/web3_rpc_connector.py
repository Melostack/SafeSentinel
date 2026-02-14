from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

class OnChainVerifier:
    def __init__(self):
        # RPCs (Priorizando chamadas seguras)
        self.rpcs = {
            "ETH": os.getenv("RPC_ETH", "https://eth.llamarpc.com"),
            "BSC": os.getenv("RPC_BSC", "https://binance.llamarpc.com"),
            "POLYGON": os.getenv("RPC_POLYGON", "https://polygon.llamarpc.com"),
            "ARBITRUM": os.getenv("RPC_ARBITRUM", "https://arbitrum.llamarpc.com")
        }

    def get_provider(self, network):
        net = network.upper()
        url = self.rpcs.get(net)
        if not url: return None
        return Web3(Web3.HTTPProvider(url))

    def verify_address(self, address, network):
        """
        Verifica na blockchain se o endereço é EOA ou Contrato.
        """
        w3 = self.get_provider(network)
        if not w3 or not w3.is_connected():
            return {"status": "RPC_OFFLINE", "type": "UNKNOWN"}

        try:
            checksum_address = w3.to_checksum_address(address)
            code = w3.eth.get_code(checksum_address)
            
            is_contract = code != b'' and code != b'\x00'
            
            return {
                "status": "SUCCESS",
                "is_contract": is_contract,
                "type": "Smart Contract" if is_contract else "Personal Wallet (EOA)",
                "explorer_url": f"https://blockscan.com/address/{address}"
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}
