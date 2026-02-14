import os
import requests
import json
from dotenv import load_dotenv

class Humanizer:
    """
    The Humanizer is the interpretive layer of SafeSentinel.
    It translates complex technical risks into human-readable mentorship messages
    using a multi-LLM provider cascade (Gemini -> Groq -> OpenRouter).
    """

    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        
        # Provider Endpoints
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

    def extract_intent(self, text: str) -> dict:
        """
        Uses Gemini to extract structured transaction data from natural language.
        """
        if not self.api_key:
            return None

        prompt = f"""
        Analise a frase do usuário sobre transferência de criptoativos e extraia as variáveis.
        FRASE: "{text}"
        REGRAS: 
        1. Retorne APENAS um JSON válido.
        2. Campos: asset, origin, destination, network, address.
        3. Use null para campos não identificados.
        """
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(f"{self.gemini_url}?key={self.api_key}", json=payload, timeout=10)
            res_json = response.json()
            text_content = res_json['candidates'][0]['content']['parts'][0]['text']
            clean_json = text_content.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except Exception:
            return None

    def humanize_risk(self, gatekeeper_data: dict) -> str:
        """
        Orchestrates the AI response using the Nudge Protocol and a provider cascade.
        """
        # 1. Primary: Gemini (Google AI Studio)
        if self.api_key:
            res = self._call_gemini(gatekeeper_data)
            if res: return res
        
        # 2. Fallback 1: Groq (Llama 3)
        if self.groq_key:
            res = self._call_groq(gatekeeper_data)
            if res: return res
            
        # 3. Fallback 2: OpenRouter (Universal Proxy)
        if self.openrouter_key:
            res = self._call_openrouter(gatekeeper_data)
            if res: return res

        # Final Deterministic Fallback
        return f"⚠️ {gatekeeper_data.get('message', 'Erro na validação.')} (Aviso: Mentor IA offline)."

    def _call_gemini(self, gatekeeper_data):
        edge_cases = self._get_edge_cases()
        prompt = self._build_prompt(gatekeeper_data, edge_cases)
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(f"{self.gemini_url}?key={self.api_key}", json=payload, timeout=10)
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            return None

    def _call_groq(self, gatekeeper_data):
        headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "Você é o SafeSentinel, mentor de segurança Web3. Use o protocolo Nudge (Metáfora, Risco, Ação). Responda em Português."},
                {"role": "user", "content": f"Interprete este risco: {gatekeeper_data}"}
            ]
        }
        try:
            response = requests.post(self.groq_url, headers=headers, json=payload, timeout=10)
            return response.json()['choices'][0]['message']['content']
        except:
            return None

    def _call_openrouter(self, gatekeeper_data):
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "HTTP-Referer": "https://safesentinel.io",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "google/gemini-2.0-flash-001",
            "messages": [
                {"role": "system", "content": "Você é o SafeSentinel, mentor de segurança Web3. Use o protocolo Nudge (Metáfora, Risco, Ação). Responda em Português."},
                {"role": "user", "content": f"Interprete este risco: {gatekeeper_data}"}
            ]
        }
        try:
            response = requests.post(self.openrouter_url, headers=headers, json=payload, timeout=15)
            return response.json()['choices'][0]['message']['content']
        except:
            return None

    def _build_prompt(self, gatekeeper_data, edge_cases):
        return f"""
        Você é o SafeSentinel, um mentor Web3 especializado em segurança On-Chain.
        Sua missão é interpretar os dados do Gatekeeper e gerar um "Veredito do Mentor" usando o PROTOCOLO NUDGE.

        PROTOCOLO NUDGE:
        1. 🧩 Metáfora: Use uma analogia do mundo real para explicar a situação técnica.
        2. 🚨 Risco Real: Explique claramente o que aconteceria com os fundos caso a transação siga.
        3. ✅ Ação Sugerida: Diga exatamente o que o usuário deve fazer para proceder com segurança.

        CONHECIMENTO DE ESPECIALISTA:
        {edge_cases}

        DADOS DA TRANSAÇÃO:
        - Status: {gatekeeper_data.get('status')} | Risco: {gatekeeper_data.get('risk')}
        - Alerta Técnico: {gatekeeper_data.get('message')}
        - Ativo: {gatekeeper_data.get('asset')} | Origem: {gatekeeper_data.get('origin_exchange')}
        - Destino: {gatekeeper_data.get('destination')} | Rede: {gatekeeper_data.get('selected_network')}
        - Trust Score: {gatekeeper_data.get('trust_score', 0)}/100
        - Dados On-Chain: {gatekeeper_data.get('on_chain', {}).get('address_type', 'EOA')}
        """

    def _get_edge_cases(self):
        paths = ['skills/edge-case-dictionary.md', 'agent/skills/custom/edge-case-dictionary.md']
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p, 'r') as f: return f.read()
                except: continue
        return ""
