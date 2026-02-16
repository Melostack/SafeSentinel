# PLAN: Phase 2 - Execution Wave 1

Esta onda foca na expansão do Sourcing Agent e na detecção de Honeypots.

<task type="auto">
  <name>Expand Sourcing Agent (Bridges & Routes)</name>
  <files>core/sourcing_agent.py</files>
  <action>
    Refatorar o SourcingAgent para usar o modelo Perplexity Sonar. 
    A lógica deve buscar por: "Qual a ponte (bridge) mais barata e segura de [NETWORK_A] para [NETWORK_B] para o token [ASSET]?".
    O retorno deve ser um JSON estruturado com 'steps', 'bridge_name' e 'estimated_fee'.
  </action>
  <verify>Rodar um teste unitário pedindo rota de ETH (Arbitrum) para ETH (Optimism).</verify>
  <done>Sourcing Agent sugerindo bridges reais.</done>
</task>

<task type="auto">
  <name>Implement Deeper Trust Analysis (Security APIs)</name>
  <files>core/gatekeeper.py, api/server.py</files>
  <action>
    Integrar o Gatekeeper com a API de segurança GoPlus (ou similar gratuita).
    Verificar se o token possui: is_honeypot, is_blacklisted, can_take_back_ownership.
    Atualizar o Trust Score no server.py para incluir esses fatores de risco.
  </action>
  <verify>Mandar um token conhecido por ser scam e ver o risco subir para CRITICAL.</verify>
  <done>Trust Score baseado em segurança de contrato, não apenas volume.</done>
</task>

<task type="auto">
  <name>Bot UX: Interactive Routes</name>
  <files>bot/telegram_bot.py</files>
  <action>
    Melhorar o comando /find. 
    Se uma rota exigir bridge, o bot deve mostrar um botão clicável para a bridge sugerida.
    Adicionar feedback visual de "Passo 1, Passo 2" na resposta do bot.
  </action>
  <verify>Executar /find e ver a lista de passos formatada.</verify>
  <done>Experiência de "Waze" para transferências complexas.</done>
</task>
