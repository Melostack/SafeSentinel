# Skill: Clarify-to-Spec Framework

**Goal:** Transform high-level, ambiguous intent (The Vibe) into a professional, actionable Technical Specification (The Spec) without making invisible assumptions.

## 🧠 The Philosophy of "Active Ignorance"
The Agent must act as if it knows nothing about the user's implicit preferences. If a requirement isn't explicitly stated or confirmed, it doesn't exist. Guessing is a failure; asking is a victory.

## 🛠️ The Discovery Framework

Before generating a `SPEC.md`, the Architect must pass the user's idea through these five filters:

### 1. The Core Objective (The "Why")
* **Prompt:** "What is the primary problem this project solves? Is it a prototype, a production tool, or a personal experiment?"
* **Goal:** Determine the level of polish and scalability required.

### 2. The User Experience (The "Who & How")
* **Prompt:** "Who is the end user? How will they interact with it? (Web, Mobile, Terminal, API call?)"
* **Goal:** Define the interface and accessibility needs.

### 3. The Technical Constraints (The "Under the Hood")
* **Prompt:** "Do you have a preferred tech stack? (Next.js, Python, Node?). Does it need to integrate with external tools (n8n, specific APIs, Crypto wallets)?"
* **Goal:** Prevent the agent from choosing a stack that the user cannot or does not want to manage.

### 4. Data & Logic (The "Brain")
* **Prompt:** "Does it need to save data? If so, what kind? Does it need authentication or complex business logic (e.g., DeFi calculations, specific automation triggers)?"
* **Goal:** Define the backend and database requirements.

### 5. Success Criteria (The "When is it done?")
* **Prompt:** "What does the final version look like? What is the single most important feature that MUST work for this to be a success?"

## 🚫 The "No-Guess" Protocol (Anti-Hallucination)

If the user gives a vague command (e.g., *"Make it look modern"*), the Agent is **forbidden** to proceed. It must offer choices:
* *Bad Response:* "I will make a dark mode UI with glassmorphism."
* *Good Response:* "Modern could mean several things. Do you prefer: A) Minimalist/SaaS style, B) High-end Editorial (like Apple), or C) Dark/Tech Vibe?"

## 📝 Output: The SPEC.md Structure

Once clarity is achieved, the output must follow this standard:
1.  **Project Title & Vision**
2.  **Confirmed Requirements** (Functional & Non-Functional)
3.  **The Tech Stack** (With justification)
4.  **Architecture Diagram** (Mermaid/Text)
5.  **TBD Section** (Requirements that are still pending or out of scope for Phases)
