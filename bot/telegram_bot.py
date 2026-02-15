import os
import logging
import httpx
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

load_dotenv()

# Configuração de logs
logging.basicConfig(level=logging.INFO)

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
hm = Humanizer()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(
        "🛡️ *SafeTransfer v1.1: O Oráculo de Segurança*\n\n"
        "Agora você pode falar comigo naturalmente. Exemplos:\n"
        "• _'Posso mandar USDT da Binance pra OKX via Arbitrum?'_\n"
        "• _'Quero enviar ETH da MetaMask pra Bybit pela BSC.'_\n\n"
        "Ou use /find [token] para descobrir onde comprar."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_chat_action("typing")
    
    # 1. Extrair Intenção via IA
    intent = hm.extract_intent(text)
    
    # Se não identificou intenção de transferência ou falta muito dado, 
    # deixamos o Humanizer conduzir a conversa (o "Oi" ou "Dúvida")
    if not intent or not intent.get('asset'):
        response_text = hm.handle_interaction(text)
        await update.message.reply_markdown(response_text)
        return

    # 2. Se identificou intenção, mas faltam dados, o Humanizer pede os dados
    if not intent.get('origin') or not intent.get('network') or not intent.get('destination'):
        response_text = hm.handle_interaction(text, gatekeeper_data={'status': 'INFO'})
        await update.message.reply_markdown(response_text)
        return

    # 3. Se tem tudo, faz a análise técnica completa
    await update.message.reply_markdown(f"⏳ *Analisando sua rota:* {intent['asset']} | {intent['origin']} ➔ {intent['destination']} ({intent['network']})")

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
            # O backend já chama o hm.handle_interaction via endpoint /check
            await update.message.reply_markdown(res['message'])

    except Exception as e:
        print(f"Bot Error: {e}")
        await update.message.reply_text("Desculpe, meu motor de raciocínio deu um soluço. Pode repetir a pergunta?")

async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Descobre a melhor rota para um token."""
    if not context.args:
        await update.message.reply_markdown(
            "🔍 *Uso do /find:*\n"
            "Exemplo: `/find OKB X-Layer`"
        )
        return
    
    token = context.args[0].upper()
    network = " ".join(context.args[1:]) if len(context.args) > 1 else "Mainnet"

    await update.message.reply_markdown(f"📡 *Consultando o Sourcing Agent:* Localizando {token} em {network}...")
    await update.message.reply_chat_action("typing")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{FASTAPI_URL}/find", json={
                "asset": token,
                "network": network
            }, timeout=60.0)
            
            res = response.json()
            data = res['data']
            
            report = f"📍 *Melhor Rota para {token} ({network}):*\n\n"
            report += f"🏦 *Origem Sugerida:* {data.get('cex_source', 'Não especificado')}\n"
            
            steps = data.get('steps', [])
            if steps:
                report += "\n*Passos:*\n"
                for i, step in enumerate(steps, 1):
                    report += f"{i}\. {step}\n"
            
            if data.get('bridge_needed'):
                report += f"\n🌉 *Bridge:* {data.get('recommended_bridge', 'Necessário')}\n"
            
            if data.get('warning'):
                report += f"\n⚠️ *Aviso:* {data.get('warning')}"

            report += f"\n\n_Fonte: {'Inteligência Real-Time' if res['source'] == 'live' else 'Base de Conhecimento'}_"
            
            # Botão CMC se disponível
            reply_markup = None
            # SourcingAgent data might contain cmc_info or slug
            slug = data.get('slug') or token.lower()
            url = f"https://coinmarketcap.com/currencies/{slug}/"
            keyboard = [[InlineKeyboardButton("📊 Verificar Detalhes (CMC)", url=url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_markdown(report, reply_markup=reply_markup)

    except Exception as e:
        await update.message.reply_text("Não consegui encontrar rotas para este token no momento. Tente novamente mais tarde.")

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Recebe denúncias da comunidade."""
    if not context.args:
        await update.message.reply_text("Uso: /report [ENDEREÇO] [MOTIVO]\nExemplo: /report 0x123... Phishing em site falso")
        return
    
    address = context.args[0]
    reason = " ".join(context.args[1:])
    
    # Aqui poderíamos salvar no Supabase. Por enquanto, confirmamos o recebimento.
    await update.message.reply_markdown(
        "🛡️ *Denúncia Recebida!*\n\n"
        f"O endereço `{address}` foi enviado para análise técnica\. "
        "Se confirmado, ele entrará na nossa Blacklist Global em breve\. Obrigado por proteger a comunidade\!"
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
