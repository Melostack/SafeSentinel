# Skill: Atomic-Step-Thinking Framework (v2.1)

**Goal:** Transform high-level tasks into error-free implementation by enforcing a granular, intent-driven, and verifiable execution process.

## 🧠 The Philosophy: "Precision Over Impulse"
* **Managed Complexity:** Complexity is unmanaged state. We grow systems through small, working, and readable parts.
* **Reversibility Rule:** Every atomic step should be easily reversible without cascading changes. This naturally enforces modularity.
* **Speed is a Byproduct:** True speed comes from not having to fix mistakes or untangle dependencies.

## 🛠️ The Execution Protocol (T-V-C-T)

### 1. Think (Atomic Deconstruction)
* **The Single Responsibility Rule:** An atom must have only ONE verifiable responsibility.
* **The Concept Limit:** If a step introduces more than one new concept or logic branch, it is NOT atomic. Break it down further.
* **Scope:** Forget line counts. If you cannot explain the step's goal in 10 seconds to a "Cold Reader," it is too complex.

### 2. Verify (The Dependency Check)
* **Zero-Magic Rule:** Confirm all imports, variables, and logic contracts exist before writing code.
* **Contract-First:** Define interfaces before implementing logic. Never code a function that calls a "placeholder."

### 3. Code (The "Anti-Overengineering" Mode)
* **The Rule of Two:** Do not create helpers, generic classes, or abstractions until a pattern appears at least TWICE. 
* **No Premature Generalization:** Code for the current need. Stay lean.

### 4. Test (The Cold Reader Check)
* **Syntactic Check:** Brackets, imports, return paths.
* **Semantic Check (The Human Factor):** "Would this code still make sense to another engineer reading it cold?" If it requires a 5-minute explanation, refactor for clarity.

## 🛑 The Stop Protocol (Smart Breaker)
The Agent must halt execution and request human intervention if uncertainty exceeds 20%:

1.  **Requirement Uncertainty (The "What/Why"):** If you are unsure of the business logic, user intent, or constraints. **Action:** STOP and hand off back to the **Architect**.
2.  **Implementation Uncertainty (The "How"):** If the technical path is unclear or the atom feels too "heavy" to execute safely. **Action:** STOP and deconstruct into smaller atoms.
3.  **Implementation Paradox:** If the current task contradicts the `SPEC.md`.
4.  **Refactor Loop:** If you find yourself changing the same logic more than twice without progress.

## 📋 Pre-Commit Checklist
* [ ] Does this atom do exactly ONE thing?
* [ ] Is this step easily reversible without cascading breaks?
* [ ] Is this code readable by a "Cold Reader"?
* [ ] Did I avoid premature abstraction (Rule of Two)?
* [ ] Is my uncertainty (Requirement & Implementation) below 20%?
