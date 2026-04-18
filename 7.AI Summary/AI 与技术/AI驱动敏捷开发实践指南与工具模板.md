---
notion-id: 24a78d23-e296-817c-bd10-c25c7cdd8f6d
Last edited time: 2025-08-09T11:46:00
Tags: []
Verification: unverified
Owner:
  - Coze-Plugin
---
# Introduction

Nice transcript — thanks for sharing. Do you want me to edit/shorten it, turn it into a video script, make slides, create agent prompts, build templates (PRD, architecture, user story), or something else?

Below are several practical things I can produce right away. Tell me which you want or pick a few and I’ll generate them.

## Quick Options I Can Deliver

- Short summary (1–2 paragraphs) suitable for a video intro.
- Tightened video script (conversational, ~3–5 minutes).
- Slide deck bullet points / chapter timestamps for the multi-video series.
- Ready-to-use agent prompts for each persona (BA, PM, Architect, PO, Scrum Master, Developer Agent).
- Templates you can drop into Cursor as Markdown: PRD, Architecture Doc, Product Backlog, Epic/Story template.
- Cursor project folder structure and recommended file naming.
- Sample initial user story (repo + infra setup) and tests.
- Cost-saving and safety checklist (when to run agents vs do manual steps).
- CI/test strategy and example test harness outline.

If you want multiple, pick 2–3 and I’ll produce them. Meanwhile, here are high-value, ready-to-use items you can copy immediately.

# Ready-to-use Items

## One-paragraph Summary

Agile AI-driven development applies classic agile roles to agent-based coding: start with an AI Business Analyst to refine the idea, hand a Project Manager agent to research and produce a PRD, let an AI Architect produce a full technical design, have a Product Owner break that into granular, ordered tasks, let a Scrum Master group tasks into epics/stories, and finally have developer agents implement one story per new chat thread with tests. The workflow enforces structure, test coverage, and repeatability, preventing “vibe coding” drift and saving time and money while enabling a scalable, maintainable product.

## High-impact Agent Prompts

### Business Analyst

**Prompt:**"You are a Business Analyst. Ask probing questions to fully define a product idea, produce a concise problem statement, user personas, key use cases, core features, and a prioritized feature list for an MVP. Return any ambiguities as follow-ups."

### Project Manager / Researcher

**Prompt:**"You are a Project Manager/researcher. Based on the BA output, research similar apps, recommended tech stacks (pros/cons), and deliver a PRD outline with MVP scope, milestones, risks, and time estimates. Cite sources and recommend 1 primary stack and 1 backup."

### Architect

**Prompt:**"You are a Software Architect. Produce a detailed architecture doc: overall system diagram, chosen languages/frameworks, directory layout, data models/schema, API contracts, auth/security, infra/deployment plan, CI/CD, and dependencies. Include rationale and trade-offs."

### Product Owner

**Prompt:**"You are the Product Owner. Convert the architecture + PRD into a sequenced task list of small, testable stories. Each story should be executable by a junior developer/agent and include acceptance criteria, dependencies, estimated effort, and required environment setup."

### Scrum Master

**Prompt:**"You are the Scrum Master. Group tasks into epics and prioritized sprints. Produce the backlog with story order, identify enabler stories (accounts, infra), and produce release milestones and a QA plan."

### Developer Agent

**Prompt:**"You are a Developer Agent. For the story provided, make a new branch, implement code, add/update tests, run tests locally, and push changes if all tests pass. If tests fail, provide a detailed error summary and a plan to fix. Respect constraints in the story file."

## Story Template

- **Title:**
- **Story ID:**
- **Epic:**
- **Priority:**
- **Description:**(short — what to implement)
- **Acceptance criteria:**(explicit, testable)
- **Inputs / Data model references:**
- **Expected outputs / UI behavior:**
- **File locations / project structure:**
- **Dependencies / earlier stories:**
- **Test cases:**(unit/integration + how-to-run)
- **Estimated effort:**
- **Notes / security concerns:**

## Example Initial Story

- **Title:**Initialize repo, baseline app, and CI
- **Story ID:**EN-001
- **Epic:**Project Setup
- **Priority:**High
- **Description:**Create repository, initialize project skeleton (frontend and backend), add README, set up basic CI pipeline, and a skeleton test that runs.
- **Acceptance criteria:**
- Repo created with branches: main and dev
- Frontend scaffold (e.g., Next.js) in /apps/web
- Backend scaffold (e.g., Node + Express or Supabase) in /apps/api
- Basic test runner configured and one passing test
- CI config (GitHub Actions) runs tests on push to dev
- **File locations:**
- /README.md
- /apps/web/...
- /apps/api/...
- **Test commands:**pnpm install && pnpm test
- **Dependencies:**none
- **Estimated effort:**2–4 hours

## Recommended Cursor Folder Structure

```plain text
aai/
  PRD.md
  architecture.md
  backlog/
    00-enablers/
      EN-001-setup-repo.md
      EN-002-setup-accounts.md
    01-auth/
      STORY-101-auth-flow.md
    02-core/
      STORY-201-core-feature.md
  docs/
    personas.md
    dev-guidelines.md
README.md

```

## Cost-saving & Safety Rules

- Do all non-code thinking steps (BA, PM, Architect, PO, Scrum Master) outside costly agent compute or in cheaper LLM modes, then paste concise Markdown into Cursor.
- Keep stories small and independent so developer agents operate in a single-chat context and don’t need long memory.
- Put infra/account setup tasks as enabler stories and do secrets/account creation manually or locally to avoid exposing credentials.
- Require tests as acceptance criteria; fail-fast if no tests exist.
- Limit expensive multimodal or deep-research queries to the PM step only, not per story.

## Test Coverage Strategy

- Start with unit tests for core functions.
- Add integration tests around API contracts.
- Add end-to-end smoke tests for key flows.
- Each story must add/modify tests; target 80% incremental coverage across core modules.
- Run tests on dev branch CI before merge to main.

# Next Steps

If you want, I can now:- Convert your entire transcript into a polished ~3-minute video script.- Generate the PRD.md and architecture.md based on an example idea (tell me your app idea).- Produce the backlog folder with 8–12 initial stories for an MVP.- Generate full prompts for Cursor developer agent with success/failure response formats.

Which one should I do next?

