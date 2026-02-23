import os
import requests
import json
import re

class Humanizer:
    def __init__(self, api_key=None):
        # Preferencia por OpenRouter devido a estabilidade de quota
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def _sanitize(self, text):
        if not text: return ""
        # Remove caracteres que podem ser usados para escapar delimitadores de prompt
        return re.sub(r'["`]', '', str(text)).strip()

    def extract_intent(self, text):
        if not self.api_key: return None
        sanitized_text = self._sanitize(text)
        
        system_prompt = "Você é um extrator de intenções JSON para transações Web3. Retorne SEMPRE um único objeto JSON com os campos: asset, origin, destination, network, address."
        user_prompt = f"Analise a seguinte frase e extraia as variáveis:\n<user_input>{sanitized_text}</user_input>"
        
        payload = {
            "model": "google/gemini-2.0-flash-001",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": { "type": "json_object" }
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=15)
            content = response.json()['choices'][0]['message']['content']
            
            data = json.loads(content) if isinstance(content, str) else content
            
            # Se a IA retornou uma lista por engano, pegamos o primeiro item
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            return data
        except Exception as e:
            print(f"Erro no extract_intent: {e}")
            return None

    def humanize_risk(self, gatekeeper_data):
        if not self.api_key: return "❌ API Key ausente."
        
        # Sanitização de campos sensíveis vindo do gatekeeper (que podem conter input do user)
        safe_msg = self._sanitize(gatekeeper_data.get('message', ''))
        risk = gatekeeper_data.get('risk', 'LOW')
        
        prefix = "ALERTA MÁXIMO" if risk == "CRITICAL_DEFCON_1" else "Mentor Web3"
        content = f"{prefix}: {safe_msg}"

        system_prompt = "Você é a MarIA, uma estrategista da Oratech didática e empática. Explique o risco de segurança Web3 usando metáforas simples."
        
        payload = {
            "model": "google/gemini-2.0-flash-001",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ]
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=15)
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Erro no humanize_risk: {e}")
            return "❌ Falha crítica na interpretação de risco."
