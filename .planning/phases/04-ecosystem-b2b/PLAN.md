# PLAN: Phase 4 - Execution Wave 1 (The Vault API)

Foco: Criar o porteiro da API para uso externo.

<task type="auto">
  <name>Database: API Keys Schema</name>
  <files>supabase_metadata/migrations/20260216010000_create_apikeys_schema.sql</files>
  <action>
    Criar tabela 'api_keys' no schema 'safetransfer'.
    Campos: key_hash, owner_name, plan_type (free/pro), requests_limit, requests_used, is_active.
  </action>
  <verify>Validar criação no Supabase.</verify>
  <done>Schema de autenticação pronto.</done>
</task>

<task type="auto">
  <name>Middleware: API Key Validation</name>
  <files>api/server.py</files>
  <action>
    Criar função `verify_api_key` no FastAPI.
    Ela deve:
    1. Ler o header 'X-API-Key'.
    2. Verificar se existe no banco e está ativa.
    3. Incrementar o contador de uso.
    4. Bloquear se estourar o limite.
  </action>
  <verify>Tentar chamar /check sem chave e com chave válida.</verify>
  <done>API protegida e pronta para B2B.</done>
</task>

<task type="auto">
  <name>Feature: Admin Key Gen</name>
  <files>scripts/generate_key.py</files>
  <action>
    Script Python simples (local) para gerar uma nova API Key, hashear e inserir no banco.
    *Segurança:* A chave raw (sk_...) é mostrada uma única vez no terminal.
  </action>
  <verify>Gerar uma chave e testar.</verify>
  <done>Sistema de emissão de chaves funcional.</done>
</task>
