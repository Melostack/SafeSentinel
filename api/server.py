from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from functools import lru_cache
from core.gatekeeper import Gatekeeper
from core.humanizer import Humanizer
from core.connectors.web3_rpc_connector import OnChainVerifier

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

@lru_cache()
def get_gatekeeper():
    return Gatekeeper()

@lru_cache()
def get_humanizer():
    return Humanizer()

@lru_cache()
def get_verifier():
    return OnChainVerifier()

@app.get("/")
def home():
    return {"status": "SafeSentinel Command Center API Operational"}

@app.post("/extract")
async def extract_intent(req: IntentRequest, hm: Humanizer = Depends(get_humanizer)):
    intent = hm.extract_intent(req.text)
    if not intent:
        raise HTTPException(status_code=400, detail="Não foi possível entender a intenção.")
    return intent

@app.post("/check")
async def check_transfer(
    req: CheckRequest,
    gk: Gatekeeper = Depends(get_gatekeeper),
    hm: Humanizer = Depends(get_humanizer),
    rpc: OnChainVerifier = Depends(get_verifier)
):
    try:
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
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
