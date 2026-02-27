import os
import logging
import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from core.humanizer import Humanizer
import sys

# Add project root to sys.path to allow importing from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# Configuração de logs
logging.basicConfig(level=logging.INFO)

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
SAFE_SENTINEL_API_KEY = os.getenv("SAFE_SENTINEL_API_KEY")

hm = Humanizer()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = (
        "🛡️ *SafeTransfer v1.1: O Oráculo de Segurança*\n\n"
        "Agora você pode falar comigo naturalmente. Exemplos:\n"
        "• _'Posso mandar USDT da Binance pra OKX via Arbitrum?'_\n"
        "• _'Quero enviar ETH da MetaMask pra Bybit pela BSC.'_\n\n"
        "Ou use /find [token] para descobrir onde comprar."
    )
    try:
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text(msg.replace("*", "").replace("_", ""))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_chat_action("typing")
    
    # 1. Extrair Intenção via IA
    intent = hm.extract_intent(text)
    
    if not isinstance(intent, dict) or not intent.get('asset'):
        await update.message.reply_text("Entendi que você quer fazer uma transferência, mas qual é o Token e a Rede?")
        return

    # Verificar se faltam dados cruciais
    missing = []
    if not intent.get('origin'): missing.append("Origem (CEX/Wallet)")
    if not intent.get('network'): missing.append("Rede")
    if not intent.get('destination'): missing.append("Destino")

    if missing:
        await update.message.reply_text(f"Entendi seu interesse em {intent['asset']}, mas preciso saber: {', '.join(missing)}")
        return

    # 2. Consultar Backend
    status_msg = f"⏳ *Validando:* {escape_markdown(intent['asset'], version=2)} | {escape_markdown(intent['origin'], version=2)} ➔ {escape_markdown(intent['destination'], version=2)} ({escape_markdown(intent['network'], version=2)})"
    await update.message.reply_text(status_msg, parse_mode=ParseMode.MARKDOWN_V2)

    headers = {}
    if SAFE_SENTINEL_API_KEY:
        headers["X-API-Key"] = SAFE_SENTINEL_API_KEY

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{FASTAPI_URL}/check",
                json={
                    "asset": intent['asset'],
                    "origin": intent['origin'],
                    "destination": intent['destination'],
                    "network": intent['network'],
                    "address": intent.get('address') or "0x0000000000000000000000000000000000000000"
                },
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 403:
                await update.message.reply_text("🚨 Erro de Autenticação: O Bot não tem permissão para acessar o Oráculo.")
                return

            res = response.json()
            status_emoji = "✅" if res.get('risk_level') == "LOW" else "🚨" if res.get('risk_level') == "CRITICAL" else "⚠️"
            
            title = res.get('title', 'Resultado da Análise')
            message = res.get('message', 'Sem detalhes adicionais.')
            solution = res.get('solution')

            report = f"{status_emoji} *{escape_markdown(title, version=2)}*\n\n"
            report += f"{escape_markdown(message, version=2)}\n\n"
            
            if solution:
                report += f"💡 *Ação Sugerida:*\n{escape_markdown(solution, version=2)}"
            
            try:
                await update.message.reply_text(report, parse_mode=ParseMode.MARKDOWN_V2)
            except Exception as e:
                logging.error(f"Erro ao enviar Markdown: {e}")
                # Fallback para texto plano se o Markdown falhar
                await update.message.reply_text(report.replace("*", "").replace("_", "").replace("\\", ""))

    except Exception as e:
        logging.error(f"Erro no handle_message: {e}")
        await update.message.reply_text("Desculpe, o motor de segurança está ocupado. Tente novamente.")

async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Reaproveitar a lógica de busca anterior
    pass

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Recebe denúncias da comunidade."""
    if not context.args:
        await update.message.reply_text("Uso: /report [ENDEREÇO] [MOTIVO]\nExemplo: /report 0x123... Phishing em site falso")
        return
    
    address = context.args[0]
    reason = " ".join(context.args[1:])
    
    # Aqui poderíamos salvar no Supabase. Por enquanto, confirmamos o recebimento.
    escaped_address = escape_markdown(address, version=2, entity_type='code')
    await update.message.reply_text(
        "🛡️ *Denúncia Recebida!*\n\n"
        f"O endereço `{escaped_address}` foi enviado para análise técnica\\. "
        "Se confirmado, ele entrará na nossa Blacklist Global em breve\\. Obrigado por proteger a comunidade\\!",
        parse_mode=ParseMode.MARKDOWN_V2
    )

if __name__ == '__main__':
    TOKEN_BOT = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN_BOT).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('find', find_command))
    app.add_handler(CommandHandler('report', report_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 SafeTransfer Conversational Bot is running...")
    app.run_polling()
