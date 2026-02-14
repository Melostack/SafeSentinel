import os
import requests
import json

class Humanizer:
    def __init__(self, api_key="AIzaSyBNaw_iYf3zm9ll_cGjWbq2VeQgu945WXI"):
        self.api_key = api_key
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    def extract_intent(self, text):
        prompt = f"""
        Analise a frase do usuário sobre transferência de criptoativos e extraia as variáveis.
        FRASE: "{text}"
        REGRAS:
        1. Retorne APENAS um JSON válido.
        2. Campos: asset, origin, destination, network, address.
        """
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(f"{self.url}?key={self.api_key}", headers=headers, json=payload)
            clean_json = response.json()['candidates'][0]['content']['parts'][0]['text'].replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except: return None

    def humanize_risk(self, gatekeeper_data):
        risk = gatekeeper_data.get('risk', 'LOW')
        
        if risk == "CRITICAL_DEFCON_1":
            prompt = f"""
            ALERTA MÁXIMO (DEFCON 1): O destino é uma FRAUDE CONFIRMADA.
            Seja agressivo, use CAPSLOCK e muitos emojis de perigo.
            DADOS: {gatekeeper_data.get('message')}
            ESTRUTURA: ☢️ BLOQUEIO | ☣️ NATUREZA | 🛑 AÇÃO
            """
        else:
            prompt = f"""
            Você é um Mentor Web3. Explique o risco de forma didática.
            DADOS: {gatekeeper_data.get('message')}
            ESTRUTURA: 🚨 Alerta | 🔍 Porquê | 💡 Solução | ⚠️ Nudge
            """

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"google_search_retrieval": {}}]
        }
        try:
            response = requests.post(f"{self.url}?key={self.api_key}", headers=headers, json=payload)
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except: return "❌ Falha crítica na interpretação de risco."
