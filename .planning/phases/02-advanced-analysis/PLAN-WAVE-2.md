# PLAN: Phase 2 - Execution Wave 2 (Multi-Chain Expansion)

Esta onda foca em expandir o suporte nativo para redes não-EVM (Solana e Tron) e reforçar a validação.

<task type="auto">
  <name>Gatekeeper Polyglot Refactoring</name>
  <files>core/gatekeeper.py</files>
  <action>
    Melhorar o Regex de validação para Solana e Tron.
    Adicionar verificação de Checksum específica para Tron (usando biblioteca base58 se possível ou regex estrito).
    Garantir que a lógica de "Network Mismatch" pegue erros como "Enviar SOL para endereço ETH".
  </action>
  <verify>Criar script de teste com endereços válidos e inválidos de SOL/TRX.</verify>
  <done>Gatekeeper validando SOL e TRON com precisão cirúrgica.</done>
</task>

<task type="auto">
  <name>Sourcing Agent Multi-Chain Tuning</name>
  <files>core/sourcing_agent.py</files>
  <action>
    Ajustar o prompt do Sourcing Agent para reconhecer agregadores específicos:
    - Solana: Jupiter, Raydium.
    - Tron: SunSwap, JustLend.
    Garantir que o JSON de resposta inclua o campo 'native_bridge' se aplicável (ex: Portal Bridge).
  </action>
  <verify>Testar /find JUP Solana e verificar se sugere Jupiter.</verify>
  <done>Sourcing Agent recomendando rotas nativas corretas.</done>
</task>

<task type="auto">
  <name>Dependency Hardening</name>
  <files>requirements.txt</files>
  <action>
    Adicionar bibliotecas 'base58' (para validação Tron/Solana) e garantir 'httpx' atualizado.
  </action>
  <verify>Instalação limpa das dependências.</verify>
  <done>Ambiente pronto para multi-chain.</done>
</task>
