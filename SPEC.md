# SPEC: SafeTransfer v1.0 (The Trust Protocol)

## 🎯 Vision
SafeTransfer is a specialized safety layer for Web3 transfers, focusing on preventing "Network Mismatch" during CEX to Wallet withdrawals.

## 🏗️ Architecture
Unidirectional agent flow: **User (Vibe) -> Architect (Spec) -> Gatekeeper (Logic) -> Humanizer (Gemini) -> Output.**

### 1. Registry Module (The Source of Truth)
- **File:** `/registry/networks.json`
- **Logic:** Map Assets (USDT, ETH) to their supported networks per destination (Binance, MetaMask, OKX).

### 2. Gatekeeper Module (Deterministic Validation)
- **Role:** Validator.
- **Tasks:**
    - Perform Address Checksum/Format validation (Regex).
    - Cross-check `network_origin` vs `network_destination` in the Registry.
    - Status codes: `SAFE`, `MISMATCH`, `INVALID_ADDRESS`.

### 3. Humanizer Module (IA Interpretation)
- **Engine:** Gemini Native.
- **Input:** Gatekeeper Logs + User Intent.
- **Output:** Educational warning in Portuguese (PT-BR) about specific loss-of-funds risks.

### 4. Sourcing Agent (SafeDiscovery)
- **Engine:** Perplexity API (Sonar Model).
- **Role:** Liquidity Explorer.
- **Function:** Find the shortest/safest route to acquire specific tokens on specific networks.
- **Cache:** `discovery_cache` table in Supabase.

## 💻 Tech Stack
- **Backend:** FastAPI.
- **Search:** Perplexity Sonar.
- **Data:** Supabase (PostgreSQL).

## ✅ Success Criterion (MVP)
Identify and explain the risk: **USDT from Binance (BEP20) -> MetaMask (ERC20-only address).**

---
*Ambiguity level: 0%. Ready for Implementation.*
