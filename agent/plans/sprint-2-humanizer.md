# 📄 Sprint 2 Plan: The Humanizer Evolution

**Agent:** Architect
**Focus:** Enhancing the AI Mentorship Layer
**Sprint Goal:** Transform technical risk data into didactic, action-oriented "Nudges" using Gemini 1.5 Flash.

---

## 🛠️ Tasks

### 1. Context Injection (Prompts)
- [ ] **1.1. Edge-Case Integration:** Incorporate the `skills/edge-case-dictionary.md` knowledge into the `humanize_risk` prompt.
- [ ] **1.2. Nudge Protocol:** Update the prompt to follow the "Nudge" style (Metaphor + Risk + Action).
- [ ] **1.3. Multilingual Support Foundation:** Ensure the system is ready for English/Portuguese toggle (though prioritizing PT-BR for now).

### 2. Backend Enhancements
- [ ] **2.1. Dynamic Context:** Ensure `api/server.py` sends `on_chain_data` (contracts, EOA vs Contract) and `trust_score` to the Humanizer.
- [ ] **2.2. Error Handling:** Create a fallback "Safe-Response" mechanism if Gemini API fails or rate-limits.

### 3. Verification & QA
- [ ] **3.1. Test Suite:** Create `tests/humanizer_test_cases.py` to simulate:
    - Case A: Binance USDT (ERC20) -> MetaMask (Polygon).
    - Case B: Sending to a Smart Contract (unintentional).
    - Case C: Low Trust Score Token (Honeypot risk).
- [ ] **3.2. Response Audit:** Use the **QA Agent** persona to review if responses are "Mentor-like" and not just "Error-like".

---

## 🎯 Success Criteria
- The "Binance -> ERC20" failure returns a metaphor-based explanation (e.g., "The Key & The Door").
- Responses include a clear "Suggested Action" (Nudge).
- Average response time for Humanization remains under 2 seconds.
