import os
import requests
import json
from dotenv import load_dotenv

class Humanizer:
    """
    The Humanizer is the interpretive layer of SafeSentinel.
    Persona: The 'Mentor Friend' - Objective, safety-first, non-technical.
    Mission: Resolve transfer doubts and source tokens without financial advice.
    """

    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.ollama_url = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

    def _get_system_prompt(self):
        return """
        VOCÊ É O SAFESENTINEL (O MENTOR AMIGO).
        Sua missão é ser o conselheiro de confiança para transferências de cripto, garantindo que o usuário nunca perca fundos por erros técnicos.
        
        DIRETRIZES DE PERSONALIDADE:
        - Objetivo e Curto: Não dê palestras. Resolva o problema de segurança.
        - Não Técnico: Use termos simples (ex: 'rede' em vez de 'mainnet', 'ponte' em vez de 'bridge').
        - Segurança em Primeiro Lugar: Se houver risco de perda de fundos, o alerta deve ser claro e imediato.
        
        PROTOCOLO NUDGE:
        1. 🧩 METÁFORA: Uma analogia simples do dia a dia para explicar o erro técnico.
        2. 🚨 RISCO REAL: Explique exatamente o que acontece com o dinheiro (ex: "fica preso no limbo").
        3. ✅ AÇÃO SUGERIDA: Diga exatamente o que o usuário deve fazer agora para operar com segurança.
        """

    def handle_interaction(self, user_input: str, gatekeeper_data: dict = None, history: list = None) -> str:
        """
        Main entry point for conversational logic.
        """
        # Se for um 'Oi' ou algo sem dados de transação
        if not gatekeeper_data or gatekeeper_data.get('status') == 'INFO':
            prompt = f"{self._get_system_prompt()}\n\nO usuário disse: '{user_input}'. Responda como o mentor, entendendo o que ele quer e pedindo os dados necessários (Ativo, Rede, Origem e Destino) se for o caso."
            return self._call_ollama_raw(prompt)

        # Se for uma análise de risco real
        edge_cases = self._get_edge_cases()
        prompt = f"""
        {self._get_system_prompt()}
        
        CONHECIMENTO TÉCNICO:
        {edge_cases}

        DADOS DA ANÁLISE:
        {json.dumps(gatekeeper_data, indent=2)}

        Gere a resposta para o usuário seguindo o protocolo Nudge. 
        Se o ativo for ETH e a rede for Polygon, avise que chegará como WETH. 
        Se faltar o MEMO em redes como XRP/TON, avise que o fundo será perdido.
        """
        return self._call_ollama_raw(prompt)

    def _call_ollama_raw(self, prompt: str) -> str:
        payload = {
            "model": "deepseek-r1:8b",
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            full_response = response.json().get('response', "")
            
            # Limpeza do DeepSeek (remover o raciocínio interno para o usuário)
            if "<think>" in full_response:
                return full_response.split("</think>")[-1].strip()
            return full_response
        except Exception as e:
            print(f"Ollama Error: {e}")
            return None # Allow fallback to other providers

    def humanize_risk(self, gatekeeper_data: dict) -> str:
        """
        Orchestrates the AI response using the Nudge Protocol and a provider cascade.
        Priority: Ollama (DeepSeek-R1 - Local & Free) -> Gemini -> Groq -> OpenRouter
        """
        # 1. Primary: Ollama
        res = self.handle_interaction("", gatekeeper_data=gatekeeper_data)
        if res and not res.startswith("Estou analisando"): return res

        # 2. Secondary: Gemini
        if self.api_key:
            res = self._call_gemini(gatekeeper_data)
            if res: return res
        
        # 3. Fallback 1: Groq
        if self.groq_key:
            res = self._call_groq(gatekeeper_data)
            if res: return res
            
        # 4. Fallback 2: OpenRouter
        if self.openrouter_key:
            res = self._call_openrouter(gatekeeper_data)
            if res: return res

        return f"⚠️ {gatekeeper_data.get('message', 'Erro na validação.')} (Aviso: Mentor IA offline)."

    def extract_intent(self, text: str) -> dict:
        prompt = f"""
        Extraia os dados desta frase de cripto: "{text}"
        Retorne APENAS um JSON puro com: asset, origin, destination, network, address.
        Use null se não souber. Exemplo: {{"asset": "USDT", "origin": "Binance", "destination": "MetaMask", "network": "ERC20", "address": null}}
        """
        
        # 1. Tenta Ollama (DeepSeek) com timeout curto
        try:
            payload = {"model": "deepseek-r1:8b", "prompt": prompt, "format": "json", "stream": False}
            print(f"DEBUG: Tentando extrair intenção via DeepSeek (Ollama)...")
            response = requests.post(self.ollama_url, json=payload, timeout=5) # Timeout de 5s
            if response.status_code == 200:
                print("DEBUG: DeepSeek respondeu com sucesso.")
                return json.loads(response.json().get('response'))
        except Exception as e:
            print(f"DEBUG: Falha no DeepSeek: {e}")

        # 2. Fallback imediato para Gemini
        if self.api_key:
            try:
                print("DEBUG: Usando Fallback Gemini para extração...")
                gemini_payload = {"contents": [{"parts": [{"text": f"Retorne apenas o JSON: {prompt}"}]}]}
                response = requests.post(f"{self.gemini_url}?key={self.api_key}", json=gemini_payload, timeout=8)
                text_res = response.json()['candidates'][0]['content']['parts'][0]['text']
                
                # Limpeza de blocos de código
                if "```json" in text_res:
                    text_res = text_res.split("```json")[1].split("```")[0].strip()
                elif "```" in text_res:
                    text_res = text_res.split("```")[1].split("```")[0].strip()
                
                return json.loads(text_res)
            except Exception as e:
                print(f"DEBUG: Falha no Fallback Gemini: {e}")

        return None

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
        Você é o SafeSentinel, o Mentor Amigo especializado em segurança de transferências Web3.
        Sua missão é gerar um "Veredito do Sentinel" usando o PROTOCOLO NUDGE.

        CONHECIMENTO DE SUPORTE:
        {edge_cases}

        DADOS DA TRANSAÇÃO:
        - Status: {gatekeeper_data.get('status')} | Risco: {gatekeeper_data.get('risk')}
        - Ativo: {gatekeeper_data.get('asset')}
        - Rota: {gatekeeper_data.get('origin_exchange')} ➔ {gatekeeper_data.get('destination')} (via rede {gatekeeper_data.get('selected_network')})
        - Trust Score: {gatekeeper_data.get('trust_score', 0)}/100
        - Tipo de Endereço: {gatekeeper_data.get('on_chain', {}).get('address_type', 'EOA')}
        - Alerta Técnico: {gatekeeper_data.get('message')}

        Lembre-se: Seja protetor e direto. O usuário conta com você para não perder dinheiro.
        """

    def _get_edge_cases(self):
        paths = ['skills/edge-case-dictionary.md', 'SafeSentinel/skills/edge-case-dictionary.md']
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p, 'r') as f: return f.read()
                except: continue
        return ""
