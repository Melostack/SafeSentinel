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
        Consulta o Perplexity Sonar com SANITIZAÇÃO de input.
        """
        if not self.api_key:
            return None, "API Key do Perplexity não configurada."

        # SANITIZAÇÃO: Permitir apenas alfanuméricos e limitando o tamanho
        clean_token = "".join(c for c in token if c.isalnum())[:10].upper()
        clean_net = "".join(c for c in target_network if c.isalnum() or c.isspace())[:20]

        if not clean_token:
            return None, "Token inválido ou malformado."

        prompt = f"""
        Você é um Arquiteto de Rotas Web3 de elite. Sua missão é proteger o capital do usuário encontrando o caminho mais eficiente para obter {clean_token} na rede {clean_net}.

        REQUISITOS DE PESQUISA (REAL-TIME):
        1. LIQUIDEZ CENTRALIZADA: Onde {token} é negociado com maior volume hoje? (Binance, OKX, Bybit, Coinbase?)
        2. SAQUE DIRETO: Alguma dessas exchanges permite saque direto para a rede {target_network}? (Ex: USDT via TRC20 ou SOL via Solana).
        3. AGREGADORES DEX (SOLANA/TRON): Se o destino for Solana, verifique se JUPITER ou RAYDIUM tem a melhor rota. Se for Tron, verifique SUNSWAP.
        4. BRIDGES: Se necessário, qual a bridge oficial (Portal, Stargate, Allbridge) é mais segura?

        FORMATO DE RESPOSTA OBRIGATÓRIO (JSON PURO):
        {{
          "steps": ["Passo 1: Compre na X", "Passo 2: Saque via rede Y", "Passo 3: Swap no Júpiter"],
          "cex_source": "Nome da melhor CEX",
          "bridge_needed": true/false,
          "recommended_bridge": "Nome da Bridge/Agregador ou 'Nativa'",
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
