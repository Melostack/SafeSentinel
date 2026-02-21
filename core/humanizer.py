import os
import requests
import json
import logging

class Humanizer:
    def __init__(self, api_key=None):
        # PROTEÇÃO: Chave agora vem estritamente do .env ou parâmetro
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    def extract_intent(self, text):
        if not self.api_key: return None
        prompt = f"""
        Analise a frase do usuário sobre transferência de criptoativos e extraia as variáveis.
        FRASE: "{text}"
        REGRAS: 1. Retorne APENAS um JSON válido. 2. Campos: asset, origin, destination, network, address.
        """
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(f"{self.url}?key={self.api_key}", headers=headers, json=payload, timeout=10)
            clean_json = response.json()['candidates'][0]['content']['parts'][0]['text'].replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except Exception as e:
            logging.error(f"Error extracting intent: {e}")
            return None

    def humanize_risk(self, gatekeeper_data):
        if not self.api_key: return "❌ API Key ausente."
        risk = gatekeeper_data.get('risk', 'LOW')
        
        if risk == "CRITICAL_DEFCON_1":
            prompt = f"ALERTA MÁXIMO: {gatekeeper_data.get('message')}"
        else:
            prompt = f"Mentor Web3: {gatekeeper_data.get('message')}"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"google_search_retrieval": {}}]
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(f"{self.url}?key={self.api_key}", headers=headers, json=payload, timeout=10)
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            logging.error(f"Error humanizing risk: {e}")
            return "❌ Falha crítica na interpretação de risco."
