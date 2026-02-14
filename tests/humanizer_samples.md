# Humanizer Samples: SafeTransfer Risk Translation

Aqui estão 5 exemplos de como a IA deve traduzir riscos complexos para os usuários.

### 1. Network Mismatch (O Clássico)
*   **Input:** USDT: Binance (BEP20) -> MetaMask (ERC20)
*   **Output Esperado:** 🚨 O Alerta: Pare! Rota Incompatível. 🔍 O Porquê: Você está enviando via BSC, mas sua MetaMask espera a rede Ethereum. 💡 A Solução: Mude para a rede ERC20. ⚠️ O Nudge: Se prosseguir, seu dinheiro sumirá no limbo entre redes.

### 2. Missing Memo (XRP/CEX)
*   **Input:** XRP: Wallet -> Binance (Rede XRP, Sem Tag)
*   **Output Esperado:** 🚨 O Alerta: Depósito em Risco. 🔍 O Porquê: Falta a Destination Tag. A Binance não saberá que o XRP é seu. 💡 A Solução: Adicione a Tag fornecida pela Binance. ⚠️ O Nudge: Se enviar sem Tag, você terá que abrir um ticket de suporte e pode levar meses para recuperar (ou nunca recuperar).

### 3. Wrapped Token Confusion
*   **Input:** ETH: MetaMask (BSC) -> Binance (Rede Ethereum)
*   **Output Esperado:** 🚨 O Alerta: Ativo Não-Nativo. 🔍 O Porquê: Você está enviando um 'Vale-ETH' (BEP20) para o endereço de ETH real. 💡 A Solução: Envie via rede ERC20 ou use uma bridge primeiro. ⚠️ O Nudge: A exchange pode não creditar ativos de redes paralelas no endereço nativo.

### 4. Wrong Format (Tron vs EVM)
*   **Input:** USDT: Binance (TRC20) -> Endereço 0x...
*   **Output Esperado:** 🚨 O Alerta: Endereço Inválido. 🔍 O Porquê: Redes Tron usam endereços que começam com 'T', você forneceu um formato Ethereum. 💡 A Solução: Verifique se o endereço está correto ou mude a rede. ⚠️ O Nudge: Transações para formatos errados costumam ser rejeitadas, mas se o app aceitar, o fundo é perdido.

### 5. High Gas Warning (Network Congestion)
*   **Input:** ETH: Transferência via Mainnet em horário de pico.
*   **Output Esperado:** 🚨 O Alerta: Taxas Abusivas. 🔍 O Porquê: A rede Ethereum está congestionada. Você vai pagar R$ 200 de taxa para enviar R$ 100. 💡 A Solução: Aguarde 2 horas ou use uma L2 (Polygon/Arbitrum). ⚠️ O Nudge: Se você ignorar, metade do seu capital será "comido" pelos mineradores.
