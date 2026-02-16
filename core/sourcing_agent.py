import os
import httpx
import json
import asyncio
from dotenv import load_dotenv

load_dotenv()

class SourcingAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        self.url = "https://api.perplexity.ai/chat/completions"

    async def find_best_route(self, token, target_network):
        """
        Consulta o Perplexity Sonar para encontrar a melhor rota de aquisição e bridge de forma ASSÍNCRONA.
        """
        if not self.api_key:
            return None, "API Key do Perplexity não configurada."

        prompt = f"""
        Você é um Arquiteto de Rotas Web3 de elite. Sua missão é proteger o capital do usuário encontrando o caminho mais eficiente para obter {token} na rede {target_network}.

        REQUISITOS DE PESQUISA (REAL-TIME):
        1. LIQUIDEZ: Onde {token} é negociado com maior volume hoje? (Binance, OKX, Bybit, Uniswap?)
        2. SAQUE DIRETO: Alguma dessas exchanges permite saque direto para a rede {target_network}?
        3. PONTES (BRIDGES): Se o saque direto não existir, qual a bridge oficial ou agregador (Stargate, Li.Fi, Jumper, Orbiter) é mais SEGURO e barato para esta rota específica?
        4. SEGURANÇA: Existe algum aviso de manutenção ou hack recente nesta rede ou bridge?

        FORMATO DE RESPOSTA OBRIGATÓRIO (JSON PURO):
        {{
          "steps": ["Passo 1: Compre na X", "Passo 2: Saque via rede Y", "Passo 3: Use bridge Z"],
          "cex_source": "Nome da melhor CEX",
          "bridge_needed": true/false,
          "recommended_bridge": "Nome da Bridge ou 'Nativa'",
          "estimated_fee_range": "Baixa/Média/Alta",
          "warning": "Aviso de segurança ou gas se houver"
        }}
        """

        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "Você é técnico, direto e responde apenas com JSON válido."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            try:
                print(f"DEBUG: Consultando Perplexity Sonar para rota de {token}...")
                response = await client.post(self.url, headers=headers, json=payload, timeout=45.0)
                response.raise_for_status()
                data = response.json()
                return json.loads(data['choices'][0]['message']['content']), None
            except Exception as e:
                print(f"DEBUG: Erro no SourcingAgent: {e}")
                return None, f"Erro na busca SafeDiscovery: {str(e)}"

if __name__ == "__main__":
    # Teste rápido via asyncio
    async def test():
        agent = SourcingAgent()
        res, err = await agent.find_best_route("ETH", "Arbitrum")
        print(json.dumps(res, indent=2) if res else err)
    
    # asyncio.run(test())
