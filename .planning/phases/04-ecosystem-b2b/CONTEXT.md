# CONTEXT: Phase 4 - Ecosystem & B2B Platform

## 🎯 Goals
1. **Monetization Ready:** Transformar a API em um produto vendável (SaaS).
2. **Interoperability:** Permitir que 'Maria', 'Oratech' e outros sistemas consumam a segurança do Sentinel.
3. **Deep Forensics:** Adicionar simulação de transações para prever o resultado exato de uma operação.

## 🧠 Architecture
- **Auth Layer:** Middleware de API Key (FastAPI) + Tabela Supabase `api_keys`.
- **Rate Limiting:** Controle de requisições por chave (ex: 100 reqs/dia no plano Free).
- **Simulator:** Integração com Tenderly ou Alchemy Simulate.
