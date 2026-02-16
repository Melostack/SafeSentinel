import secrets
import hashlib
import os
from datetime import datetime
from dotenv import load_dotenv
from core.connectors.supabase_connector import SupabaseConnector

load_dotenv()

def generate_api_key(owner_name, plan="FREE", limit=100):
    """
    Gera uma nova API Key segura para o SafeSentinel.
    """
    # 1. Gerar a chave crua (Secure Token)
    prefix = "sk_live_"
    random_part = secrets.token_urlsafe(24)
    raw_key = f"{prefix}{random_part}"
    
    # 2. Gerar o hash para armazenamento
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    
    # 3. Salvar no Supabase
    supabase = SupabaseConnector()
    if not supabase.client:
        print("❌ Erro: Não foi possível conectar ao Supabase.")
        return

    try:
        data = {
            "key_prefix": raw_key[:12],
            "key_hash": key_hash,
            "owner_name": owner_name,
            "plan_type": plan,
            "requests_limit": limit
        }
        
        supabase.client.schema("safetransfer").table("api_keys").insert(data).execute()
        
        print("
" + "="*50)
        print("🛡️  SAFESENTINEL - NOVA CHAVE DE API GERADA")
        print("="*50)
        print(f"OWNER: {owner_name}")
        print(f"PLAN:  {plan} ({limit} reqs/dia)")
        print("-"*50)
        print(f"CHAVE: {raw_key}")
        print("-"*50)
        print("⚠️  AVISO: Guarde esta chave agora. Ela NÃO será mostrada novamente.")
        print("="*50 + "
")
        
    except Exception as e:
        print(f"❌ Erro ao salvar chave no banco: {e}")

if __name__ == "__main__":
    name = input("Nome do Proprietário da Chave: ")
    plan = input("Plano (FREE/PRO): ").upper() or "FREE"
    limit = int(input("Limite de Requisições (padrão 100): ") or 100)
    
    generate_api_key(name, plan, limit)
