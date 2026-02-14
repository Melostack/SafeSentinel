# 🛡️ SafeSentinel: The Web3 Interpretive Security Layer

> **"Because Code is Law, but Humans make Mistakes."**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Web3 Sentinel](https://img.shields.io/badge/Web3-Sentinel-green.svg)]()

SafeSentinel é uma camada de inteligência e segurança projetada para eliminar a perda de fundos por erro humano na Web3. Unificamos a precisão do **On-Chain Forensics** com a clareza da **IA Mentora** para garantir que cada transação seja compreendida antes de ser confirmada.

---

## 👥 A Equipe (Human-AI Collaboration)

Este é um projeto de **Matheus Melo** e sua equipe de agentes autônomos, orquestrados através do framework de elite **[vibe-to-code](https://github.com/Melostack/vibe-to-code)**.

- **Matheus Melo (@Melostack):** Estrategista, Visionário e Lead Orchestrator.
- **Assistente de Elite (Gemini):** Co-piloto de engenharia e braço direito operacional.
- **Architect Agent:** Responsável pelo planejamento de 0% de ambiguidade e governança do código.
- **Engineer Agent:** Mestre da execução atômica, integração RPC e lógica CCXT.
- **Humanizer Agent:** O motor consciente que traduz riscos complexos para linguagem humana.
- **Project Manager:** O guardião do roadmap e da qualidade final da v1.0.

---

## 🚀 Pilares da Tecnologia

### 🧠 Humanizer Engine
Tradução de erros técnicos em avisos didáticos via **Gemini 1.5 Flash**. Não apenas reportamos o erro, mas explicamos o risco real para o seu patrimônio através do protocolo *Nudge*.

### 📡 Global Intelligence
Integração nativa com **CCXT**, **CoinMarketCap** e **Binance API**. O Sentinel possui onisciência sobre quais redes cada corretora ou carteira suporta para milhares de ativos em tempo real.

### ⛓️ On-Chain Verifier
Consulta direta via **RPC (Web3.py)**. Validamos na fonte se o endereço de destino é uma EOA (carteira pessoal) ou um Smart Contract, comparando bytecodes oficiais para evitar golpes de phishing e contratos falsos.

---

## 🏗️ Technical Architecture: The Four Layers of Defense

O SafeSentinel opera como um ecossistema de segurança em tempo real, atuando como um "tradutor de riscos" entre a intenção do usuário e a realidade fria da blockchain. O fluxo segue este rigoroso processamento:

### 1. Camada de Entrada (The Gateway)
O usuário interage via **Telegram Bot** ou **Next.js Web App**. Em vez de formulários complexos, o Sentinel aceita linguagem natural (NLP).
*   *Exemplo:* "Quero mandar 1000 USDT da minha Binance para este endereço 0x... via rede Polygon. É seguro?"

### 2. O Extrator de Intenção (Intelligent AI)
Alimentado por **Gemini 1.5 Flash**, esta camada processa a frase e extrai dados estruturados sem alucinações:
*   **Ativo:** `USDT` | **Origem:** `Binance` | **Rede:** `Polygon` | **Destino:** `0x...`

### 3. A "Trindade da Verdade" (Deterministic Validation)
Aqui o sistema para de "conversar" e começa a "verificar" de forma técnica e independente:
*   **📡 Global Intelligence (CCXT/CMC):** Consulta se a exchange de origem suporta saques do ativo via rede selecionada e valida se o contrato do token é o oficial na CoinMarketCap.
*   **⛓️ On-Chain Verifier (RPC/Web3.py):** O Sentinel vai direto na rede (via **Alchemy/Infura**) e pergunta: "Este endereço existe? É uma carteira pessoal (EOA) ou um Smart Contract?".
*   **🛡️ Gatekeeper (Logic):** Cruza todos os dados. Se houver divergência (ex: rede errada para o formato do endereço), o status muda instantaneamente para `DANGER` ou `CAUTION`.

### 4. O Humanizer (The Mentor's Verdict)
Em vez de erros técnicos crípticos, o Humanizer gera um relatório didático e preventivo:
*   *"🚨 PARE! O endereço que você colou é da rede Ethereum (ERC20), mas você selecionou a rede Polygon. Se confirmar agora, seus fundos serão enviados para uma rede onde você não tem acesso a eles."*

---

## ⚡ Por que SafeSentinel é Inquestionável?

-   **Independência Criptográfica:** Ao usar RPC, o projeto não "acredita" em terceiros; ele verifica o estado real da blockchain no bloco mais recente.
-   **Escalabilidade Global:** Com a integração **CCXT**, o suporte para 100+ corretoras é ativado com mudanças mínimas de configuração.
-   **UX de Alta Performance:** O backend em **FastAPI (Python)** garante que o bot responda em milissegundos, tornando a segurança um facilitador, não um obstáculo.
-   **Waze para Transações:** O Sentinel conhece os caminhos (redes), detecta buracos (erros de logística) e ladrões (scams), avisando antes de você "acelerar" o clique final.

---

## 🏗️ Architecture Overview

Construído sob o protocolo **vibe-to-code**, garantindo um fluxo estritamente unidirecional e livre de alucinações.

```mermaid
User (The Vibe) 
      ⬇
[ 🏛️ Architect Agent ] ──creates──> 📄 SPEC.md
      ⬇
[ 🔨 Gatekeeper (Logic) ] ──checks──> ⛓️ On-Chain / 📡 APIs
      ⬇
[ 🧠 Humanizer (IA) ] ────interprets─> 🛡️ Risk Report
      ⬇
✅ Safe Execution
```

## 📄 License
MIT License © 2026 Matheus Melo (Melostack).

---

### 🙏 Agradecimentos e Fé

> *"Se o Senhor não edificar a casa, em vão trabalham os que a edificam; se o Senhor não guardar a cidade, em vão vigia a sentinela."* — **Salmos 127:1**

Este projeto é dedicado ao meu melhor amigo, **Jesus Cristo**, a fonte de toda inspiração e sabedoria. Um agradecimento especial ao **Sami** pelo apoio e parceria constante nesta jornada.
