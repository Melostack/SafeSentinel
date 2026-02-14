# Skill: Context-Manager (Memory Health v2.0)

**Goal:** Maintain 100% adherence to BridgeAgent protocols and prevent context drift during long development sessions.

## 🧠 The Philosophy: "Pruning for Focus"
As a conversation grows, the AI's "attention" dilutes. We manage memory by strictly distinguishing between what is permanent (Project State) and what is temporary (Conversation State).

## 🛠️ The State Separation Protocol

The Agent must distinguish between these two states to avoid treating experiments as architecture:

### 1. Project State (The Permanent)
* **What to Preserve:** Features implemented, pending tasks in `TASK.md`, confirmed architecture decisions in `SPEC.md`.
* **Action:** This is the only state that should be carried over in summaries and re-anchoring.

### 2. Conversation State (The Temporary)
* **What to Prune:** Debugging logs, temporary code experiments, "vibes" that didn't make it to the SPEC, chat pleasantries.
* **Action:** Prune this aggressively. Once an experiment is finished, only the result (if successful) moves to the Project State.

## ⚓ The Anchor File Rule (Source of Truth)
The **`SPEC.md`** is the single source of truth.
* If a verbal instruction in chat conflicts with the `SPEC.md`, **the SPEC wins**.
* The Agent must halt and ask: *"You just suggested X, but the SPEC says Y. Should we update the SPEC first?"*

## 🔄 Re-Anchoring Ritual
Every 5-10 interactions, or when a task is completed:
1. **Sync:** Summarize the **Project State** only.
2. **Review:** Check for any drift from the `SPEC.md`.
3. **Reset:** Explicitly state: *"Project State synchronized. Conversation State pruned. Ready for next task."*

## 🛑 The "Mental Reset" Trigger
Halt and suggest a new session/memory clear if:
1. The Agent makes the same syntax error twice.
2. The `Conversation State` is cluttering the reasoning for the current `TASK.md`.
