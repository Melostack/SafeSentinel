import os
import sys

# Forçar a remoção do diretório raiz do path temporariamente para importar a lib oficial
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root in sys.path:
    sys.path.remove(project_root)

from supabase import create_client, Client

# Restaurar o path para outras importações internas funcionarem
sys.path.append(project_root)

from dotenv import load_dotenv

load_dotenv()

class SupabaseConnector:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            self.client = None
        else:
            self.client = create_client(url, key)

    def log_verification(self, query_payload, status, response_time_ms=0):
        """Salva logs de verificação no schema safetransfer."""
        if not self.client: return
        try:
            data = {
                "query_payload": query_payload,
                "status": status,
                "response_time_ms": response_time_ms
            }
            # Especificando o schema 'safetransfer'
            self.client.schema("safetransfer").table("verification_logs").insert(data).execute()
        except Exception as e:
            print(f"Erro ao logar no Supabase: {str(e)}")

    def get_discovery_cache(self, token, network):
        """Busca no cache de descoberta."""
        if not self.client: return None
        try:
            res = (self.client.schema("safetransfer")
                .table("discovery_cache")
                .select("*")
                .eq("token_symbol", token.upper())
                .eq("target_network", network.upper())
                .execute())
            return res.data[0] if res.data else None
        except: return None

    def save_discovery_cache(self, token, network, route_data):
        """Salva resultado no cache de descoberta."""
        if not self.client: return
        try:
            data = {
                "token_symbol": token.upper(),
                "target_network": network.upper(),
                "route_data": route_data
            }
            self.client.schema("safetransfer").table("discovery_cache").insert(data).execute()
        except Exception as e:
            print(f"Erro ao salvar cache: {str(e)}")
