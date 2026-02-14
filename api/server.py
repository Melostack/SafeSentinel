from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.gatekeeper import Gatekeeper
from core.humanizer import Humanizer
from core.sourcing_agent import SourcingAgent
from core.connectors.web3_rpc_connector import OnChainVerifier
from core.connectors.supabase_connector import SupabaseConnector
from core.connectors.cmc_api import CMCConnector
import os
import time
import math
from datetime import datetime

app = FastAPI()

def calculate_trust_score(token_data):
    """
    Calcula um Trust Score de 0 a 100.
    Score = w1*V + w2*A + w3*C
    """
    if not token_data: return 0
    score = 0
    
    # 1. Volume (24h) - Peso 40%
    # Normalização: Log scale. 10M USD = Full Score.
    volume = token_data.get('volume_24h', 0)
    if volume > 0:
        v_score = min(40, (math.log10(max(1, volume)) / 7) * 40)
        score += v_score

    # 2. Idade (Age) - Peso 30%
    # Normalização: 2 anos (730 dias) = Full Score.
    date_added_str = token_data.get('date_added')
    if date_added_str:
        try:
            # Ex: "2013-04-28T00:00:00.000Z"
            date_added = datetime.fromisoformat(date_added_str.replace('Z', '+00:00'))
            age_days = (datetime.now(date_added.tzinfo) - date_added).days
            a_score = min(30, (age_days / 730) * 30)
            score += a_score
        except: pass

    # 3. Verificação (Contract/Platforms) - Peso 30%
    # Se tem múltiplos contratos ou é Top 100 CMC
    contracts = token_data.get('contracts', [])
    if len(contracts) > 0:
        score += 30
    
    return round(score, 1)

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

class FindRequest(BaseModel):
    asset: str
    network: str

@app.get("/")
def home():
    return {"status": "SafeSentinel Command Center API Operational"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/find")
async def find_route(req: FindRequest):
    # ... logic already implemented ...

@app.get("/search-token/{symbol}")
async def search_token(symbol: str):
    cmc = CMCConnector()
    data, error = cmc.get_token_metadata(symbol)
    if error:
        raise HTTPException(status_code=404, detail=error)
    
    data['trust_score'] = calculate_trust_score(data)
    return data

@app.post("/extract")
async def extract_intent(req: IntentRequest):
    hm = Humanizer()
    intent = hm.extract_intent(req.text)
    if not intent:
        raise HTTPException(status_code=400, detail="Não foi possível entender a intenção.")
    return intent

@app.post("/check")
async def check_transfer(req: CheckRequest):
    start_time = time.time()
    try:
        gk = Gatekeeper()
        hm = Humanizer()
        rpc = OnChainVerifier()
        supabase = SupabaseConnector()
        cmc = CMCConnector()

        # 0. Intel Prévia (Trust Score)
        token_intel, _ = cmc.get_token_metadata(req.asset)
        trust_score = calculate_trust_score(token_intel) if token_intel else 0

        # 1. Validação On-Chain (RPC)
        on_chain_data = rpc.verify_address(req.address, req.network)

        # 2. Lógica de Negócio (Gatekeeper)
        gk_res = gk.check_compatibility(req.origin, req.destination, req.asset, req.network, req.address)
        
        # Adicionar Intel ao contexto do Humanizer
        gk_res.update({
            "asset": req.asset,
            "origin_exchange": req.origin,
            "destination": req.destination,
            "selected_network": req.network,
            "on_chain": on_chain_data,
            "trust_score": trust_score,
            "volume_24h": token_intel.get('volume_24h') if token_intel else 0
        })

        response_payload = {}

        if gk_res['status'] != 'SAFE':
            explanation = hm.humanize_risk(gk_res)
            response_payload = {
                "status": gk_res['status'],
                "risk_level": gk_res['risk'],
                "title": "Alerta de Segurança",
                "message": explanation,
                "on_chain": on_chain_data,
                "trust_score": trust_score,
                "token_intel": token_intel
            }
        else:
            explanation = hm.humanize_risk(gk_res)
            response_payload = {
                "status": "SAFE",
                "risk_level": "LOW",
                "title": "Caminho Seguro",
                "message": explanation,
                "on_chain": on_chain_data,
                "trust_score": trust_score,
                "token_intel": token_intel
            }
        
        # 3. Log no Supabase
        end_time = time.time()
        duration = int((end_time - start_time) * 1000)
        supabase.log_verification(
            query_payload=req.model_dump(),
            status=response_payload['status'],
            response_time_ms=duration
        )

        return response_payload

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
