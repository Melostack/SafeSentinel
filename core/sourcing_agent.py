import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class SourcingAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        self.url = "https://api.perplexity.ai/chat/completions"

    def find_best_route(self, token, target_network):
        """
        Consulta o Perplexity para encontrar a melhor rota de aquisição e bridge.
        """
        if not self.api_key:
            return None, "API Key do Perplexity não configurada."

        prompt = f"""
        Você é um explorador de liquidez Web3 de elite. 
        Sua missão é encontrar a rota mais curta, barata e segura para adquirir o token {token} na rede {target_network}.
        
        PESQUISA:
        1. Em quais exchanges (CEX) {token} tem mais liquidez?
        2. Qual a rede de saque disponível nessas CEXs?
        3. Se {token} não estiver na rede {target_network} nativamente, qual a bridge oficial ou agregador (Li.Fi, Jumper) mais confiável?
        
        RESPOSTA:
        Retorne um JSON com:
        - steps: [lista de passos curtos]
        - cex_source: [melhor corretora]
        - bridge_needed: [bool]
        - recommended_bridge: [nome da bridge se necessário]
        - warning: [aviso de gas ou segurança]
        """

        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "Seja técnico, preciso e retorne apenas JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return json.loads(data['choices'][0]['message']['content']), None
        except Exception as e:
            return None, f"Erro na busca SafeDiscovery: {str(e)}"

if __name__ == "__main__":
    # Teste rápido (Mock)
    print("--- Sourcing Agent: Iniciando rascunho de busca ---")
    # agent = SourcingAgent()
    # print(agent.find_best_route("OKB", "X Layer"))
