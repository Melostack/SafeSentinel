# 🛡️ SafeSentinel: The Web3 Interpretive Security Layer

> **"Because Code is Law, but Humans make Mistakes."**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Web3 Sentinel](https://img.shields.io/badge/Web3-Sentinel-green.svg)]()

SafeSentinel é uma camada de inteligência e segurança projetada para eliminar a perda de fundos por erro humano na Web3. Unificamos a precisão do **On-Chain Forensics** com a clareza da **IA Mentora** para garantir que cada transação seja compreendida antes de ser confirmada.

## 🚀 Pilares da Tecnologia

### 🧠 Humanizer Engine
Tradução de erros técnicos em avisos didáticos via **Gemini 1.5 Flash**. Não apenas reportamos o erro, mas explicamos o risco real para o seu patrimônio através do protocolo *Nudge*.

### 📡 Global Intelligence
Integração nativa com **CCXT**, **CoinMarketCap** e **Binance API**. O Sentinel possui onisciência sobre quais redes cada corretora ou carteira suporta para milhares de ativos em tempo real.

### ⛓️ On-Chain Verifier
Consulta direta via **RPC (Web3.py)**. Validamos na fonte se o endereço de destino é uma EOA (carteira pessoal) ou um Smart Contract, comparando bytecodes oficiais para evitar golpes de phishing e contratos falsos.

### 💬 Conversational Sentinel
Interface via **Telegram Bot** com extração de intenção por Processamento de Linguagem Natural (NLP). Fale com o Sentinel como se estivesse falando com um mentor de segurança.

## 🏗️ Architecture Overview

The flow is strictly unidirectional to prevent logic loops and hallucinations:

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

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- API Keys: Gemini, Perplexity, CoinMarketCap.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Melostack/SafeSentinel.git
   cd SafeSentinel
   ```

2. **Setup Secrets:**
   ```bash
   cp .env.example .env
   # Edit .env with your keys
   ```

3. **Run the Sentinel:**
   ```bash
   # Terminal 1: Backend API
   python3 api/server.py
   
   # Terminal 2: Telegram Bot
   python3 bot/telegram_bot.py
   ```

## 📄 License
MIT License © 2026 Matheus Melo (Melostack) - Part of the **vibe-to-code** ecosystem.
