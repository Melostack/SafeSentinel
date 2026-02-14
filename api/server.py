from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.gatekeeper import Gatekeeper
from core.humanizer import Humanizer
from core.sourcing_agent import SourcingAgent
import logging

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Habilitar CORS para o Frontend Next.js
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

class DiscoveryRequest(BaseModel):
    token: str
    network: str

@app.get("/")
def home():
    return {"status": "SafeSentinel API Operational"}

@app.post("/check")
async def check_transfer(req: CheckRequest):
    try:
        gk = Gatekeeper('core/registry/networks.json')
        hm = Humanizer()

        is_valid_format, format_msg = gk.validate_address_format(req.address, req.network)
        gk_res = gk.check_compatibility(req.origin, req.destination, req.asset, req.network, req.address)
        
        gk_res.update({
            "asset": req.asset,
            "origin_exchange": req.origin,
            "destination": req.destination,
            "selected_network": req.network
        })

        if gk_res['status'] != 'SAFE' or not is_valid_format:
            explanation = hm.humanize_risk(gk_res)
            return {
                "status": gk_res['status'],
                "risk_level": gk_res['risk'],
                "title": "Alerta de Segurança" if "CRITICAL" in gk_res['risk'] else "Atenção",
                "message": explanation,
                "solution": "Verifique a rede de origem e destino." if not is_valid_format else gk_res['message']
            }
        
        return {
            "status": "SAFE",
            "risk_level": "LOW",
            "title": "Caminho Seguro",
            "message": "A rota selecionada é compatível com o endereço de destino.",
            "solution": "Pode prosseguir com a transferência."
        }
    except Exception as e:
        logger.exception(f"Error in /check: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/find-token")
async def find_token_route(req: DiscoveryRequest):
    try:
        source = SourcingAgent()
        route, error = source.find_best_route(req.token, req.network)
        if error:
            logger.error(f"Error finding route: {error}")
            raise HTTPException(status_code=500, detail="Error processing request")
        return route
    except Exception as e:
        logger.exception(f"Error in /find-token: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
