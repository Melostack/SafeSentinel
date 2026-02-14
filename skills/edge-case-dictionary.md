# Skill: Edge-Case-Dictionary (Web3 Safety)

**Goal:** Provide specific diagnostic knowledge for non-obvious Web3 risks.

## 🔍 1. Falta de Memo/Tag (CEX Focus)
*   **Context:** Redes como XRP, XLM, EOS e às vezes TON/Cosmos.
*   **Risk:** Sem o Memo, a CEX recebe o fundo na carteira "mãe", mas não sabe a qual conta creditar. O dinheiro fica no limbo operacional da exchange.
*   **Nudge:** "Imagine enviar uma carta para um prédio enorme sem o número do apartamento. O correio entrega no prédio, mas ninguém recebe a carta."

## 🌉 2. Tokens Wrapped (Liquidity Trap)
*   **Context:** Enviar ETH para a rede BSC (vira binance-peg ETH) ou BTC para Ethereum (WBTC).
*   **Risk:** O usuário acha que tem o ativo nativo, mas tem um "recibo" dele em outra rede. Pode haver falta de liquidez ou impossibilidade de usar em dApps nativos.
*   **Nudge:** "Você trocou seu ouro por um vale-ouro em outro país. Para ter o ouro de volta, terá que cruzar a fronteira (bridge) e pagar pedágio (taxas)."

## 🪞 3. Endereços Espelhados (The 0x Trap)
*   **Context:** O mesmo endereço 0x funciona em ETH, BSC, Polygon, etc.
*   **Risk:** O usuário assume que porque o endereço é igual, a rede não importa.
*   **Nudge:** "Ter a mesma chave não significa que ela abre todas as portas. Você está tentando usar a chave da sua casa na porta do trabalho."
