# CONTEXT: Phase 3 - Proactive Alerts & Monitoring

## 🎯 Goals
1. **Wallet Registration:** Permitir que o usuário "assine" o Sentinel para uma carteira específica.
2. **On-Chain Watchdog:** Monitorar eventos de transferência via WebSockets/RPC para detectar saques para redes incompatíveis ou endereços de risco.
3. **Smart Notifications:** Enviar o "Veredito do Sentinel" proativamente via Telegram.

## 🧠 Technical Pattern
- **Watcher:** Um script em background (Python) rodando em loop ou usando WebSockets da Alchemy/Infura.
- **Queue:** Uso de Redis (opcional) ou loop simples na VPS para processar eventos.
- **Persistence:** Tabela `monitored_wallets` no Supabase.
