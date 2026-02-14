import os
import requests
import json

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
            response = requests.post(f"{self.url}?key={self.api_key}", headers=headers, json=payload)
            clean_json = response.json()['candidates'][0]['content']['parts'][0]['text'].replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except: return None

    def humanize_risk(self, gatekeeper_data):
        if not self.api_key: return "❌ API Key ausente."
        risk = gatekeeper_data.get('risk', 'LOW')
        message = gatekeeper_data.get('message', '')
        
        prompt = f"""
        Você é o SafeSentinel, um mentor Web3 especializado em segurança On-Chain.
        Sua missão é explicar de forma humana, técnica e direta o risco detectado pelo Gatekeeper.
        
        DADOS DO GATEKEEPER:
        - Status: {gatekeeper_data.get('status')}
        - Risco: {risk}
        - Alerta: {message}
        - Ativo: {gatekeeper_data.get('asset')}
        - Origem: {gatekeeper_data.get('origin_exchange')}
        - Destino: {gatekeeper_data.get('destination')}
        - Rede: {gatekeeper_data.get('selected_network')}
        - Trust Score: {gatekeeper_data.get('trust_score')}
        - Volume 24h (USD): {gatekeeper_data.get('volume_24h')}
        
        REGRAS DE RESPOSTA:
        1. Se o risco for CRITICAL ou HIGH, seja enfático sobre o perigo de perda de fundos.
        2. Se o Volume 24h for < 100000 e o token for conhecido (ex: USDT, ETH), avise sobre possível baixa liquidez ou erro de market data.
        3. Se o Volume 24h for muito baixo (< 5000), adicione: 'Cuidado: Baixa liquidez detectada para este ativo. Risco de slippage ou honeypot.'.
        4. Use um tom profissional mas acessível.
        5. Idioma: Português do Brasil.
        """

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(f"{self.url}?key={self.api_key}", headers=headers, json=payload)
            res_json = response.json()
            if 'candidates' in res_json:
                return res_json['candidates'][0]['content']['parts'][0]['text']
            return f"⚠️ {message}"
        except Exception as e: 
            return f"⚠️ Erro na interpretação (IA Offline): {message}"
