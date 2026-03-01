from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from core.gatekeeper import Gatekeeper
from core.humanizer import Humanizer
from core.sourcing_agent import SourcingAgent
from core.connectors.web3_rpc_connector import OnChainVerifier
import os
import secrets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CheckRequest(BaseModel):
    asset: str = Field(..., max_length=100)
    origin: str = Field(..., max_length=100)
    destination: str = Field(..., max_length=100)
    network: str = Field(..., max_length=100)
    address: str = Field(..., max_length=200)

class IntentRequest(BaseModel):
    text: str = Field(..., max_length=2000)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def get_api_key(api_key_header: str = Security(api_key_header)):
    expected_api_key = os.getenv("SAFE_SENTINEL_API_KEY")
    if not expected_api_key:
        logger.error("CRITICAL: SAFE_SENTINEL_API_KEY is not set in environment.")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if not secrets.compare_digest(api_key_header, expected_api_key):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key_header

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
        logger.error(f"Error processing transfer check: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
