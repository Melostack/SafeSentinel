import os
import requests
import json

class Humanizer:
    def __init__(self, api_key=None):
        # Preferencia por OpenRouter devido a estabilidade de quota
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def extract_intent(self, text):
        if not self.api_key: return None
        prompt = f"""
        Analise a frase do usuário sobre transferência de criptoativos e extraia as variáveis.
        FRASE: "{text}"
        REGRAS: 1. Retorne APENAS um JSON válido. 2. Campos: asset, origin, destination, network, address.
        """
        payload = {
            "model": "google/gemini-2.0-flash-001",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": { "type": "json_object" }
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        try:
            response = requests.post(self.url, headers=headers, json=payload)
            return response.json()['choices'][0]['message']['content']
        except: return None

    def humanize_risk(self, gatekeeper_data):
        if not self.api_key: return "❌ API Key ausente."
        risk = gatekeeper_data.get('risk', 'LOW')
        
        if risk == "CRITICAL_DEFCON_1":
            msg = f"ALERTA MÁXIMO: {gatekeeper_data.get('message')}"
        else:
            msg = f"Mentor Web3: {gatekeeper_data.get('message')}"

        payload = {
            "model": "google/gemini-2.0-flash-001",
            "messages": [{"role": "user", "content": msg}]
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        try:
            response = requests.post(self.url, headers=headers, json=payload)
            return response.json()['choices'][0]['message']['content']
        except: return "❌ Falha crítica na interpretação de risco."
