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
  <name>Implementation: Wallet Watchdog Script</name>
  <files>core/watchdog.py</files>
  <action>
    Criar script que lê as carteiras do banco e consulta o histórico de transações recentes (via Explorer APIs ou RPC).
    Se uma transação nova for detectada, enviar os dados para o Gatekeeper analisar.
  </action>
  <verify>Rodar o script e ver se ele detecta uma transação de teste.</verify>
  <done>Watchdog detectando transações em tempo real.</done>
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
