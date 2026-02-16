import os
import httpx
import json
import asyncio
from dotenv import load_dotenv

class Humanizer:
    """
    The Humanizer is the interpretive layer of SafeSentinel.
    Persona: The 'Mentor Friend' - Objective, safety-first, non-technical.
    """

    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        # Túnel de Elite: host.docker.internal (Docker -> VPS Host)
        self.ollama_url = os.getenv("OLLAMA_URL") or "http://host.docker.internal:11434/api/generate"
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

    def _get_system_prompt(self):
        return """
        VOCÊ É O SAFESENTINEL (O MENTOR AMIGO).
        Sua missão é ser o conselheiro de confiança para transferências de cripto.
        
        PROTOCOLO NUDGE:
        1. 🧩 METÁFORA: Uma analogia simples para o problema.
        2. 🚨 RISCO REAL: O que acontece com o dinheiro.
        3. ✅ AÇÃO SUGERIDA: O que o usuário deve fazer.
        """

    async def handle_interaction(self, user_input: str, gatekeeper_data: dict = None) -> str:
        if not gatekeeper_data or gatekeeper_data.get('status') == 'INFO':
            prompt = f"{self._get_system_prompt()}\n\nO usuário disse: '{user_input}'. Responda como o mentor."
            return await self._call_ollama_raw(prompt)

        edge_cases = self._get_edge_cases()
        prompt = f"{self._get_system_prompt()}\n\nCONHECIMENTO: {edge_cases}\n\nDADOS: {json.dumps(gatekeeper_data)}\n\nGere a resposta Nudge."
        return await self._call_ollama_raw(prompt)

    async def _call_ollama_raw(self, prompt: str) -> str:
        """Chamada ASSÍNCRONA ao Qwen2.5 na VPS."""
        payload = {"model": "qwen2.5:7b", "prompt": prompt, "stream": False}
        async with httpx.AsyncClient() as client:
            try:
                print(f"DEBUG: Consultando Qwen2.5 na VPS: {self.ollama_url}")
                response = await client.post(self.ollama_url, json=payload, timeout=180.0)
                if response.status_code == 200:
                    return response.json().get('response', "")
                return None
            except Exception as e:
                print(f"DEBUG: Falha no Ollama: {e}")
                return None

    async def humanize_risk(self, gatekeeper_data: dict) -> str:
        """Cascade: Ollama -> Gemini -> Groq."""
        res = await self.handle_interaction("", gatekeeper_data=gatekeeper_data)
        if res: return res

        if self.api_key:
            res = await self._call_gemini(gatekeeper_data)
            if res: return res
        
        if self.groq_key:
            res = await self._call_groq(gatekeeper_data)
            if res: return res

        return f"⚠️ {gatekeeper_data.get('message', 'Erro na validação.')}"

    async def extract_intent(self, text: str) -> dict:
        prompt = f"Extraia JSON (asset, origin, destination, network, address) de: '{text}'. Use null se não souber."
        payload = {"model": "qwen2.5:7b", "prompt": prompt, "format": "json", "stream": False}
        
        async with httpx.AsyncClient() as client:
            try:
                # Timeout de Elite para CPU: 120s
                response = await client.post(self.ollama_url, json=payload, timeout=120.0)
                if response.status_code == 200:
                    return json.loads(response.json().get('response'))
            except:
                pass

            # Fallback Gemini para extração
            if self.api_key:
                try:
                    p = {"contents": [{"parts": [{"text": f"Retorne apenas JSON: {prompt}"}]}]}
                    r = await client.post(f"{self.gemini_url}?key={self.api_key}", json=p, timeout=10.0)
                    t = r.json()['candidates'][0]['content']['parts'][0]['text']
                    if "```json" in t: t = t.split("```json")[1].split("```")[0].strip()
                    elif "```" in t: t = t.split("```")[1].split("```")[0].strip()
                    return json.loads(t)
                except: pass
        return None

    async def _call_gemini(self, gatekeeper_data):
        edge_cases = self._get_edge_cases()
        prompt = f"Você é o SafeSentinel. Interprete: {gatekeeper_data}. Use o protocolo Nudge. Conhecimento: {edge_cases}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{self.gemini_url}?key={self.api_key}", json=payload, timeout=15.0)
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            except: return None

    async def _call_groq(self, gatekeeper_data):
        headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "Você é o SafeSentinel. Use o protocolo Nudge. Responda em Português."},
                {"role": "user", "content": f"Interprete: {gatekeeper_data}"}
            ]
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.groq_url, headers=headers, json=payload, timeout=15.0)
                return response.json()['choices'][0]['message']['content']
            except: return None

    def _get_edge_cases(self):
        paths = ['skills/edge-case-dictionary.md', 'SafeSentinel/skills/edge-case-dictionary.md']
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p, 'r') as f: return f.read()
                except: continue
        return ""
