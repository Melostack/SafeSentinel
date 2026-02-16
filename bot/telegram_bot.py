import os
import logging
import httpx
import sys

# Forçar a inclusão do diretório raiz no path do Python
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from core.humanizer import Humanizer

# Garantir carregamento robusto do .env na VPS
env_path = os.path.join(os.getcwd(), '.env')
load_dotenv(env_path)

# Configuração de logs
logging.basicConfig(level=logging.INFO)

# Configuração de rede interna Docker SAMI
FASTAPI_URL = os.getenv("FASTAPI_URL") or "http://safesentinel-api:8000"
hm = Humanizer()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(
        "🛡️ *SafeTransfer v1.2: Conectado à VPS*\n\n"
        "Agora estou usando o motor Qwen2.5 de alta performance.\n"
        "Exemplo: _'Posso mandar USDT da Binance pra MetaMask?'_"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    print(f"DEBUG: Mensagem recebida: {text}")
    await update.message.reply_chat_action("typing")
    
    # 1. Extrair Intenção via IA (Agora assíncrono)
    intent = await hm.extract_intent(text)
    
    # Se não identificou intenção de transferência ou falta muito dado
    if not intent or not intent.get('asset'):
        response_text = await hm.handle_interaction(text)
        await update.message.reply_markdown(response_text)
        return

    # 2. Se identificou intenção, mas faltam dados
    if not intent.get('origin') or not intent.get('network') or not intent.get('destination'):
        response_text = await hm.handle_interaction(text, gatekeeper_data={'status': 'INFO'})
        await update.message.reply_markdown(response_text)
        return

    # 3. Análise técnica via Backend VPS
    await update.message.reply_markdown(f"⏳ *Analisando rota:* {intent['asset']} | {intent['origin']} ➔ {intent['destination']}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{FASTAPI_URL}/check", json={
                "asset": intent['asset'],
                "origin": intent['origin'],
                "destination": intent['destination'],
                "network": intent['network'],
                "address": intent.get('address') or "0x0000000000000000000000000000000000000000"
            }, timeout=45.0)
            
            res = response.json()
            await update.message.reply_markdown(res['message'])

    except Exception as e:
        print(f"Bot Error: {e}")
        await update.message.reply_text("Desculpe, meu motor de raciocínio deu um soluço. Pode repetir a pergunta?")

if __name__ == '__main__':
    TOKEN_BOT = os.getenv("TELEGRAM_BOT_TOKEN")
    print(f"🛡️ [VPS-DOCKER] Iniciando Bot SafeSentinel. Backend: {FASTAPI_URL}")
    
    app = ApplicationBuilder().token(TOKEN_BOT).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()
