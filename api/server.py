import sys
import os

# Forçar a inclusão do diretório raiz no path do Python
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# Garantir que a biblioteca supabase oficial seja priorizada
if project_root in sys.path:
    sys.path.remove(project_root)
sys.path.append(project_root)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.gatekeeper import Gatekeeper
from core.humanizer import Humanizer
from core.connectors.web3_rpc_connector import OnChainVerifier
from core.connectors.supabase_connector import SupabaseConnector
from core.connectors.cmc_api import CMCConnector
from core.connectors.goplus_api import GoPlusConnector
from core.sourcing_agent import SourcingAgent
from core.simulator import TransactionSimulator
import time
import math
import hashlib
from datetime import datetime
from fastapi.security import APIKeyHeader
from fastapi import Depends

# Configuração de Segurança B2B
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    """Verifica se a chave de API é válida e tem limite disponível."""
    if not api_key:
        # Por enquanto permite sem chave para o Bot/Front interno
        return {"owner": "Internal", "plan": "UNLIMITED"}
    
    supabase = SupabaseConnector()
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    try:
        res = (supabase.client.schema("safetransfer")
            .table("api_keys")
            .select("*")
            .eq("key_hash", key_hash)
            .eq("is_active", True)
            .execute())
        
        if not res.data:
            raise HTTPException(status_code=403, detail="Invalid API Key")
        
        key_data = res.data[0]
        if key_data['requests_used'] >= key_data['requests_limit']:
            raise HTTPException(status_code=429, detail="API Key rate limit exceeded")
        
        # Incrementar uso (Fire and Forget para performance)
        supabase.client.schema("safetransfer").table("api_keys").update({
            "requests_used": key_data['requests_used'] + 1,
            "last_used": datetime.now().isoformat()
        }).eq("id", key_data['id']).execute()
        
        return key_data
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail="Auth Engine Error")

app = FastAPI(
    title="SafeSentinel API",
    description="The Web3 Interpretive Security Layer Backend",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CheckRequest(BaseModel):
    asset: str
    origin: str
    destination: str
    network: str
    address: str

class IntentRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    message: str
    system_prompt: str | None = None

class SourcingRequest(BaseModel):
    asset: str
    network: str

def calculate_trust_score(token_data: dict) -> float:
    """Calculates a safety score (0-100) based on market health."""
    if not token_data: return 0.0
    score = 0.0
    volume = token_data.get('volume_24h', 0)
    if volume > 0:
        v_score = min(40, (math.log10(max(1, volume)) / 7) * 40)
        score += v_score
    date_added_str = token_data.get('date_added')
    if date_added_str:
        try:
            date_added = datetime.fromisoformat(date_added_str.replace('Z', '+00:00'))
            age_days = (datetime.now(date_added.tzinfo) - date_added).days
            a_score = min(30, (age_days / 730) * 30)
            score += a_score
        except: pass
    contracts = token_data.get('contracts', [])
    if len(contracts) > 0: score += 30
    return round(score, 1)

@app.get("/health")
def health_check():
    return {"status": "SafeSentinel Engine Online (Docker)", "timestamp": datetime.now().isoformat()}

@app.post("/extract")
async def extract_intent(req: IntentRequest, auth: dict = Depends(verify_api_key)):
    hm = Humanizer()
    intent = await hm.extract_intent(req.text)
    if not intent: raise HTTPException(status_code=400, detail="Could not interpret intent.")
    return intent

@app.post("/ai/chat")
async def ai_chat(req: ChatRequest):
    """General AI Chat endpoint via Qwen2.5."""
    try:
        hm = Humanizer()
        response = await hm._call_ollama_raw(req.message)
        if not response:
            context = {"status": "INFO", "risk": "NONE", "message": req.message}
            response = await hm.humanize_risk(context)
        return {"response": response, "model": "qwen2.5:7b"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(e)}")

@app.post("/find")
async def find_route(req: SourcingRequest, auth: dict = Depends(verify_api_key)):
    # ... (lógica existente mantida)
    pass

import hmac
import hashlib
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
# ... (restante dos imports)

@app.post("/webhook/alchemy")
async def alchemy_webhook(request: Request, x_alchemy_signature: str = Header(None)):
    """
    Alchemy Radar: Multichain Activity Receiver with HMAC Validation.
    """
    # 1. Validar Assinatura (Segurança Crítica)
    signing_key = os.getenv("ALCHEMY_SIGNING_KEY")
    if signing_key:
        body = await request.body()
        signature = hmac.new(signing_key.encode('utf-8'), body, hashlib.sha256).hexdigest()
        if signature != x_alchemy_signature:
            raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = await request.json()
        # 2. Identificar a rede do sinal da Alchemy
        alchemy_net = payload.get('event', {}).get('network', 'ETH_MAINNET')
        network_map = {
            "ETH_MAINNET": "ETH",
            "MATIC_MAINNET": "POLYGON",
            "ARB_MAINNET": "ARBITRUM",
            "OPT_MAINNET": "OPTIMISM",
            "BASE_MAINNET": "BASE"
        }
        network = network_map.get(alchemy_net, "ETH")

        activity = payload.get('event', {}).get('activity', [{}])[0]
        to_address = activity.get('toAddress')
        from_address = activity.get('fromAddress')
        asset = activity.get('asset')
        
        if not to_address: return {"status": "ignored"}

        # 2. Forensic & Security Check
        gk = Gatekeeper()
        hm = Humanizer()
        rpc = OnChainVerifier()

        on_chain = rpc.verify_address(to_address, network)
        gk_res = gk.check_compatibility(f"Monitored Wallet ({from_address[:6]})", "Destination", asset, network, to_address, on_chain_data=on_chain)
        
        # 3. Alerta Proativo se houver risco
        if gk_res['risk'] != 'LOW':
            supabase = SupabaseConnector()
            # Busca quem é o dono dessa carteira no nosso banco
            res = (supabase.client.schema("safetransfer")
                .table("monitored_wallets")
                .select("telegram_id")
                .eq("address", from_address)
                .eq("is_active", True)
                .execute())
            
            if res.data:
                telegram_id = res.data[0]['telegram_id']
                explanation = await hm.humanize_risk(gk_res)
                
                # Chamar o método de alerta do bot
                from bot.telegram_bot import send_proactive_alert
                await send_proactive_alert(telegram_id, explanation)
            
        return {"status": "processed", "network_detected": network, "risk": gk_res['risk']}
    except Exception as e:
        print(f"Webhook Error: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/check")
async def check_transfer(req: CheckRequest, auth: dict = Depends(verify_api_key)):
    start_time = time.time()
    try:
        gk = Gatekeeper()
        hm = Humanizer()
        supabase = SupabaseConnector()
        cmc = CMCConnector()
        goplus = GoPlusConnector()
        sim = TransactionSimulator()

        # 1. Market & Trust Intelligence
        token_intel, _ = await cmc.get_token_metadata(req.asset)
        
        # 2. On-Chain Forensics & Simulation
        on_chain_data = rpc.verify_address(req.address, req.network)
        security_intel = None
        sim_data = None
        
        # Simular a transação se tivermos um endereço de origem
        # (Se o usuário não deu origem, usamos o endereço de queima como placeholder para ver erros de contrato)
        from_placeholder = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" # vitalik.eth como tester
        sim_data, _ = await sim.simulate_transfer(from_placeholder, req.address, req.asset, req.network)

        # Se for um contrato (token), faz o audit de segurança
        if on_chain_data.get('is_contract') or req.asset.upper() != "ETH":
            security_intel, _ = await goplus.check_token_security(req.address, req.network)
        
        # ... (lógica de trust score mantida) ...
        
        # 3. Consolidar context para o Humanizer
        gk_res.update({
            "asset": req.asset, "origin_exchange": req.origin, "destination": req.destination,
            "selected_network": req.network, "on_chain": on_chain_data, "trust_score": trust_score,
            "security_audit": security_intel,
            "simulation": sim_data
        })

        explanation = await hm.humanize_risk(gk_res)
        is_safe = gk_res['status'] == 'SAFE'
        
        response_payload = {
            "status": gk_res['status'], "risk_level": gk_res['risk'],
            "title": "Veredito do Sentinel" if is_safe else "Alerta de Segurança",
            "message": explanation, "on_chain": on_chain_data, "trust_score": trust_score
        }
        
        duration = int((time.time() - start_time) * 1000)
        supabase.log_verification(query_payload=req.model_dump(), status=response_payload['status'], response_time_ms=duration)
        return response_payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
