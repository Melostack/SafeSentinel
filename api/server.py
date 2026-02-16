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
import time
import math
from datetime import datetime

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
async def extract_intent(req: IntentRequest):
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
async def find_route(req: SourcingRequest):
    """
    SafeDiscovery: Finds the best route to acquire a token on a specific network.
    Uses Perplexity Sonar via SourcingAgent.
    """
    try:
        agent = SourcingAgent()
        supabase = SupabaseConnector()
        
        # 1. Check Cache
        cached = supabase.get_discovery_cache(req.asset, req.network)
        if cached:
            return {"status": "SUCCESS", "source": "cache", "data": cached['route_data']}
        
        # 2. Search Live
        data, error = await agent.find_best_route(req.asset, req.network)
        if error:
            raise HTTPException(status_code=500, detail=error)
        
        # 3. Save Cache
        supabase.save_discovery_cache(req.asset, req.network, data)
        
        return {"status": "SUCCESS", "source": "live", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Discovery Error: {str(e)}")

@app.post("/check")
async def check_transfer(req: CheckRequest):
    start_time = time.time()
    try:
        gk = Gatekeeper()
        hm = Humanizer()
        rpc = OnChainVerifier()
        supabase = SupabaseConnector()
        cmc = CMCConnector()
        goplus = GoPlusConnector()

        # 1. Market & Trust Intelligence
        token_intel, _ = await cmc.get_token_metadata(req.asset)
        
        # 2. On-Chain Forensics & Security Audit
        on_chain_data = rpc.verify_address(req.address, req.network)
        security_intel = None
        
        # Se for um contrato (token), faz o audit de segurança
        if on_chain_data.get('is_contract') or req.asset.upper() != "ETH":
            security_intel, _ = await goplus.check_token_security(req.address, req.network)

        trust_score = calculate_trust_score(token_intel) if token_intel else 0
        
        # Ajustar Trust Score com base na análise de segurança (GoPlus)
        if security_intel:
            trust_score = max(0, trust_score - security_intel['trust_score_impact'])

        # 3. Security Logic (Gatekeeper)
        gk_res = gk.check_compatibility(req.origin, req.destination, req.asset, req.network, req.address, on_chain_data=on_chain_data, security_audit=security_intel)
        
        # Consolidar context para o Humanizer
        gk_res.update({
            "asset": req.asset, "origin_exchange": req.origin, "destination": req.destination,
            "selected_network": req.network, "on_chain": on_chain_data, "trust_score": trust_score,
            "security_audit": security_intel
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
