# PLAN: Phase 3 - Execution Wave 1

Esta onda foca no registro de carteiras e no esqueleto do Watchdog.

<task type="auto">
  <name>Database: Monitored Wallets Schema</name>
  <files>supabase_metadata/migrations/20260216000000_create_monitoring_schema.sql</files>
  <action>
    Criar tabela 'monitored_wallets' no schema 'safetransfer'.
    Campos: id, user_id (Telegram ID), address, network, created_at, last_scan.
  </action>
  <verify>Verificar se a tabela aparece no Supabase.</verify>
  <done>Schema de monitoramento pronto.</done>
</task>

<task type="auto">
  <name>API: Alchemy Webhook Receiver</name>
  <files>api/server.py</files>
  <action>
    Criar o endpoint POST /webhook/alchemy.
    Este endpoint deve processar o payload da Alchemy (Address Activity) e extrair: from, to, value, asset, network.
  </action>
  <verify>Simular um POST no endpoint e ver se o log do servidor processa os dados.</verify>
  <done>Backend pronto para receber sinais da Alchemy.</done>
</task>

<task type="auto">
  <name>Logic: Proactive Risk Analysis</name>
  <files>api/server.py, core/humanizer.py</files>
  <action>
    Integrar o fluxo de análise proativa: 
    Webhook -> Gatekeeper Check -> Humanizer (Alerta Urgente) -> Telegram Send.
  </action>
  <verify>Gerar um alerta fake e conferir se ele chega no Telegram com o tom de "Vigia".</verify>
  <done>Fluxo de monitoramento completo.</done>
</task>

<task type="auto">
  <name>Bot: /monitor Command</name>
  <files>bot/telegram_bot.py</files>
  <action>
    Adicionar comando /monitor [endereço] [rede].
    O bot deve salvar a carteira no banco para monitoramento proativo.
  </action>
  <verify>Usar o comando no Telegram e conferir o banco.</verify>
  <done>Usuários podem assinar alertas de segurança.</done>
</task>
