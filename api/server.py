from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.gatekeeper import Gatekeeper
from core.humanizer import Humanizer
from core.sourcing_agent import SourcingAgent
from core.connectors.web3_rpc_connector import OnChainVerifier
import os
import secrets
import logging

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    expected_key = os.getenv("SAFE_SENTINEL_API_KEY")
    if not expected_key:
        logging.error("CRITICAL: SAFE_SENTINEL_API_KEY is not set in the environment.")
        raise HTTPException(status_code=500, detail="Server Configuration Error")

    if not api_key_header or not secrets.compare_digest(api_key_header, expected_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key_header

app = FastAPI()

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

@app.get("/")
def home():
    return {"status": "SafeSentinel Command Center API Operational"}

@app.post("/extract")
async def extract_intent(req: IntentRequest, api_key: str = Depends(get_api_key)):
    hm = Humanizer()
    intent = hm.extract_intent(req.text)
    if not intent:
        raise HTTPException(status_code=400, detail="Não foi possível entender a intenção.")
    return intent

@app.post("/check")
async def check_transfer(req: CheckRequest, api_key: str = Depends(get_api_key)):
    try:
        gk = Gatekeeper()
        hm = Humanizer()
        rpc = OnChainVerifier()

        # 1. Validação On-Chain (RPC)
        on_chain_data = rpc.verify_address(req.address, req.network)

        # 2. Lógica de Negócio (Gatekeeper)
        gk_res = gk.check_compatibility(req.origin, req.destination, req.asset, req.network, req.address)
        
        gk_res.update({
            "asset": req.asset,
            "origin_exchange": req.origin,
            "destination": req.destination,
            "selected_network": req.network,
            "on_chain": on_chain_data
        })

        if gk_res['status'] != 'SAFE':
            explanation = hm.humanize_risk(gk_res)
            return {
                "status": gk_res['status'],
                "risk_level": gk_res['risk'],
                "title": "Alerta de Segurança",
                "message": explanation,
                "on_chain": on_chain_data
            }
        
        return {
            "status": "SAFE",
            "risk_level": "LOW",
            "title": "Caminho Seguro",
            "message": "A rota selecionada foi validada e está livre de riscos conhecidos.",
            "on_chain": on_chain_data
        }
    except Exception as e:
        logging.error("Internal Server Error in /check", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred during the check.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
