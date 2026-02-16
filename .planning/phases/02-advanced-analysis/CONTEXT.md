# CONTEXT: Phase 2 - Advanced Sourcing & Analysis

## 🎯 Goals
1. **SafeDiscovery Expansion:** O Sourcing Agent deve ser capaz de sugerir bridges (pontes) seguras quando o envio direto entre CEX e Wallet for inviável.
2. **Honeypot Detection:** Integrar análise de contratos para detectar funções maliciosas (ex: "blacklist", "mintable") em tokens de baixa liquidez.
3. **Multi-Chain Awareness:** Adicionar suporte especializado para Solana e Tron no Sourcing Agent.

## 🧠 Technical Pattern
- **Engine:** Perplexity Sonar (via `sourcing_agent.py`) para busca de liquidez em tempo real.
- **On-Chain:** Uso de APIs de segurança (como GoPlus ou RugDoc) como suporte ao Gatekeeper.
- **UX:** O Bot deve oferecer o comando `/find [TOKEN] [NETWORK]` com rotas passo-a-passo.
