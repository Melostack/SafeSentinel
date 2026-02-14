# BridgeAgent Workflow

O fluxo de trabalho padrão do BridgeAgent é projetado para garantir máxima fidelidade entre a ideia e a execução.

## Fase 1: Captação da Vibe (Input)
O usuário fornece a descrição inicial. Não há necessidade de termos técnicos.
- **Trigger:** "Quero criar um app de..." ou "Crie um componente que..."
- **Objetivo:** Capturar o sentimento e a utilidade.

## Fase 2: Arquitetura e Entrevista (Spec)
O Agente **Architect** assume o controle.
1.  Analisa a Vibe.
2.  Faz perguntas de clarificação (Edge cases, Stack, Preferências).
3.  Gera o `requirements.md` e o `SPEC.md`.
- **Artefato:** Documentação técnica aprovada pelo usuário.

## Fase 3: Decomposição e Planejamento (Roadmap)
O Arquiteto quebra a Spec em **Milestones** e **Phases**.
- Cada fase deve ter um objetivo testável.
- As tarefas são distribuídas para os agentes especialistas.

## Fase 4: Execução Especializada (Delegation)
- **Engineer Agent:** Recebe a lógica e os requisitos de backend/funcionalidade.
- **Designer Agent:** Recebe as diretrizes de UI/UX e estilo.
Ambos trabalham sob a supervisão das diretrizes do Arquiteto.

## Fase 5: Ciclo de Qualidade (Review & QA)
Um agente independente (ou o próprio Arquiteto em modo QA) verifica:
- O código funciona?
- Ele segue o `SPEC.md`?
- Ele quebra algum padrão de segurança?

## Fase 6: Entrega e Validação (Output)
O código é apresentado ao usuário.
- **UAT (User Acceptance Testing):** O usuário valida a "Vibe" final.
- Se houver gaps, o fluxo volta para a Fase 4.

---
*Este workflow minimiza alucinações ao forçar a IA a concordar com um plano escrito antes de tocar no código.*
