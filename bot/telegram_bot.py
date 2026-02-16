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
        "• _'Posso mandar USDT da Binance pra MetaMask?'_\n"
        "• Use /find [token] [rede] para descobrir rotas.\n"
        "• Use /monitor [endereço] [rede] para vigiar sua carteira.\n"
        "• Use /report [endereço] para denunciar golpes."
    )

async def monitor_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ativa o monitoramento de uma carteira."""
    if len(context.args) < 2:
        await update.message.reply_markdown("🔍 *Uso do /monitor:* `/monitor [ENDEREÇO] [REDE]`\nExemplo: `/monitor 0x123... ETH`")
        return
    
    address = context.args[0]
    network = context.args[1].upper()
    telegram_id = update.effective_user.id
    
    from core.connectors.supabase_connector import SupabaseConnector
    db = SupabaseConnector()
    
    success, error = db.add_monitored_wallet(telegram_id, address, network)
    
    if success:
        await update.message.reply_markdown(
            f"✅ *Vigia Ativado\!*\n"
            f"O SafeSentinel agora monitora a carteira `{address}` na rede `{network}`\.\n"
            "Qualquer transação suspeita detectada enviará um alerta aqui\!"
        )
    else:
        await update.message.reply_text(f"❌ Erro ao ativar vigia: {error}")

async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Descobre a melhor rota para um token."""
    if not context.args:
        await update.message.reply_markdown("🔍 *Uso do /find:* `/find OKB X-Layer`")
        return
    
    token = context.args[0].upper()
    network = " ".join(context.args[1:]) if len(context.args) > 1 else "Mainnet"

    status_msg = await update.message.reply_markdown(f"📡 *Consultando Sourcing Agent:* Localizando {token} em {network}...")
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
            report += f"🏦 *Origem Sugerida:* `{data.get('cex_source', 'Não especificado')}`\n"
            
            steps = data.get('steps', [])
            if steps:
                report += "\n*Guia Passo a Passo:*\n"
                for i, step in enumerate(steps, 1):
                    # Formatação mais bonita para os passos
                    report += f"{i}️⃣ {step}\n"
            
            keyboard = []
            if data.get('bridge_needed'):
                bridge_name = data.get('recommended_bridge', 'Bridge')
                report += f"\n🌉 *Bridge Recomendada:* {bridge_name}\n"
                
                # Adicionar botão para a bridge se for conhecida (Ex: Jumper, Stargate)
                bridge_urls = {
                    "Jumper": "https://jumper.exchange",
                    "Stargate": "https://stargate.finance",
                    "Li.Fi": "https://jumper.exchange",
                    "Orbiter": "https://orbiter.finance"
                }
                url = bridge_urls.get(bridge_name, "https://google.com/search?q=" + bridge_name + "+crypto+bridge")
                keyboard.append([InlineKeyboardButton(f"🚀 Abrir {bridge_name}", url=url)])
            
            if data.get('warning'):
                report += f"\n⚠️ *Aviso:* _{data.get('warning')}_"

            reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
            
            await status_msg.delete()
            await update.message.reply_markdown(report, reply_markup=reply_markup)

    except Exception as e:
        await update.message.reply_text("Não consegui encontrar rotas para este token no momento.")

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (lógica existente mantida)
    pass

async def send_proactive_alert(telegram_id: str, message: str):
    """Envia um alerta urgente para o usuário."""
    # Como o Bot e a API estão no mesmo ambiente ou rede, podemos usar um webhook interno ou instanciar o bot
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    from telegram import Bot
    bot_app = Bot(token=token)
    try:
        await bot_app.send_message(chat_id=telegram_id, text=f"🚨 *ALERTA DO VIGIA SENTINEL*\n\n{message}", parse_mode='Markdown')
    except Exception as e:
        print(f"Erro ao enviar alerta proativo: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    print(f"🛡️ [RECEBIDO]: {text}")
    await update.message.reply_chat_action("typing")
    
    # 1. Extrair Intenção via IA
    intent = await hm.extract_intent(text)
    
    # --- NOVA LÓGICA: Monitoramento via Linguagem Natural ---
    monitor_keywords = ["vigie", "monitore", "vigiar", "monitorar", "avise", "alerta"]
    if any(key in text.lower() for key in monitor_keywords) and intent and intent.get('address'):
        address = intent['address']
        network = intent.get('network') or 'ETH'
        telegram_id = update.effective_user.id
        
        from core.connectors.supabase_connector import SupabaseConnector
        db = SupabaseConnector()
        success, error = db.add_monitored_wallet(telegram_id, address, network)
        
        if success:
            await update.message.reply_markdown(f"✅ *Entendido\!* Comecei a vigiar a carteira `{address}` na rede `{network}` para você\.")
        else:
            await update.message.reply_text(f"Tive um problema ao registrar: {error}")
        return

    # --- Lógica de Transferência (Existente) ---
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
    app.add_handler(CommandHandler('find', find_command))
    app.add_handler(CommandHandler('monitor', monitor_command))
    app.add_handler(CommandHandler('report', report_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()
