import sys
import os

# Fix for ModuleNotFoundError: No module named 'core'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.gatekeeper import Gatekeeper
from core.humanizer import Humanizer
from core.connectors.web3_rpc_connector import OnChainVerifier
from core.connectors.supabase_connector import SupabaseConnector
from core.connectors.cmc_api import CMCConnector
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

def calculate_trust_score(token_data: dict) -> float:
    """
    Calculates a safety score (0-100) based on market health and history.
    Algorithm: 40% Volume + 30% Age + 30% Contract Verification.
    """
    if not token_data:
        return 0.0
    
    score = 0.0
    
    # 1. Volume (24h) - Peso 40% (Benchmark: $10M)
    volume = token_data.get('volume_24h', 0)
    if volume > 0:
        v_score = min(40, (math.log10(max(1, volume)) / 7) * 40)
        score += v_score

    # 2. Token Age - Peso 30% (Benchmark: 2 years)
    date_added_str = token_data.get('date_added')
    if date_added_str:
        try:
            date_added = datetime.fromisoformat(date_added_str.replace('Z', '+00:00'))
            age_days = (datetime.now(date_added.tzinfo) - date_added).days
            a_score = min(30, (age_days / 730) * 30)
            score += a_score
        except:
            pass

    # 3. On-Chain Footprint - Peso 30%
    contracts = token_data.get('contracts', [])
    if len(contracts) > 0:
        score += 30
    
    return round(score, 1)

@app.get("/health")
def health_check():
    """Returns the operational status of the engine."""
    return {"status": "SafeSentinel Engine Online", "timestamp": datetime.now().isoformat()}

@app.post("/extract")
async def extract_intent(req: IntentRequest):
    """Extracts structured intent from natural language using Gemini."""
    hm = Humanizer()
    intent = hm.extract_intent(req.text)
    if not intent:
        raise HTTPException(status_code=400, detail="Could not interpret intent.")
    return intent

@app.post("/ai/chat")
async def ai_chat(req: ChatRequest):
    """
    General AI Chat endpoint for the Oratech Ecosystem (e.g. Maria).
    Uses the local DeepSeek-R1 via Ollama as priority.
    """
    try:
        hm = Humanizer()
        # Create a mock gatekeeper context for a generic chat
        context = {
            "status": "INFO",
            "risk": "NONE",
            "message": req.message,
            "custom_prompt": req.system_prompt
        }
        
        # We can use a direct call to _call_ollama if we want to skip the humanizer nudge protocol
        # or just use the humanizer for consistency.
        # Let's use Ollama directly for a cleaner "Brain" response.
        response = hm._call_ollama({
            "status": "CHAT",
            "message": f"SYSTEM: {req.system_prompt}\nUSER: {req.message}"
        }) if req.system_prompt else hm._call_ollama({"status": "CHAT", "message": req.message})

        if not response:
            # Fallback to Gemini via humanize_risk logic
            response = hm.humanize_risk(context)

        return {"response": response, "model": "deepseek-r1:8b"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(e)}")

@app.post("/check")
async def check_transfer(req: CheckRequest):
    """
    Core verification engine.
    Orchestrates Gatekeeper, RPC Forensics, and Humanizer interpretation.
    """
    start_time = time.time()
    try:
        gk = Gatekeeper()
        hm = Humanizer()
        rpc = OnChainVerifier()
        supabase = SupabaseConnector()
        cmc = CMCConnector()

        # 1. Market & Trust Intelligence
        token_intel, _ = cmc.get_token_metadata(req.asset)
        trust_score = calculate_trust_score(token_intel) if token_intel else 0

        # 2. On-Chain Forensics
        on_chain_data = rpc.verify_address(req.address, req.network)

        # 3. Security Logic (Gatekeeper)
        gk_res = gk.check_compatibility(req.origin, req.destination, req.asset, req.network, req.address)
        
        # Consolidate context for the Humanizer
        gk_res.update({
            "asset": req.asset,
            "origin_exchange": req.origin,
            "destination": req.destination,
            "selected_network": req.network,
            "on_chain": on_chain_data,
            "trust_score": trust_score,
            "volume_24h": token_intel.get('volume_24h', 0) if token_intel else 0
        })

        # 4. Human Interpretation (Nudge Protocol)
        explanation = hm.humanize_risk(gk_res)
        
        is_safe = gk_res['status'] == 'SAFE'
        response_payload = {
            "status": gk_res['status'],
            "risk_level": gk_res['risk'],
            "title": "Veredito do Sentinel" if is_safe else "Alerta de Segurança",
            "message": explanation,
            "on_chain": on_chain_data,
            "trust_score": trust_score,
            "token_intel": token_intel
        }
        
        # 5. Telemetry & Logging
        duration = int((time.time() - start_time) * 1000)
        supabase.log_verification(
            query_payload=req.model_dump(),
            status=response_payload['status'],
            response_time_ms=duration
        )

        return response_payload

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
