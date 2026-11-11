---
name: frontier-craft
description: High-tier prompting and visual-craft workflow for frontier models (Gemini Pro, Claude Opus, GPT-5 Pro/Reasoning) to produce exceptional, anti-slop UIs, creative artifacts, and complex deliverables. Use when targeting top-tier models, avoiding generic AI aesthetics, or running screenshot critique loops.
---

# Frontier Exceptional Craft & Anti-Slop Workflow

## 1. Frontier Model Prompt Discipline (Avoid Over-Prompting)
- **No Step-by-Step Micromanagement**: Never instruct frontier reasoning models to "think step by step" or paste brittle legacy patches; specify **Goal + Acceptance Criteria + Hard Constraints + High Effort**.
- **Leave Creative Room**: Provide sharp design boundaries and let the model synthesize within them rather than micro-dictating every token.

## 2. Two-Pass Aesthetic & Anti-Slop Protocol (UI / Visual Artifacts)
1. **Pass 1 — Design Manifesto (Before Coding)**:
   - Define a 2–5 word concrete vibe grounded in the subject matter.
   - Declare explicit **Color Tokens** (`OKLCH`/HEX), **Typography Pairing** (display + body, banning default Inter/Roboto/Arial clichés), **Structural Layout** (asymmetry/bento/editorial rather than generic 3-card grids), **3 Design Dials** (Variance, Motion Intensity, Visual Density), and **One Signature Move**.
   - Enforce **Anti-Slop Bans**: no unrequested purple-indigo gradients, no cliché template chrome (`01/02/03` without sequence, decorative glows, generic placeholder copy).
2. **Pass 2 — Execution & Visual Critique Loop**:
   - Build modular components anchored to the token dictionary, implementing loading/empty/hover/focus states.
   - To avoid endless **"screenshot-and-tweak" regressions**, write a **Slop Inventory + What-to-Keep + Surgical Plan** before editing code, stabilize fonts/animations (`document.fonts.ready`), and inspect multi-viewport screenshots (`375px`, `768px`, `1440px`) or separate Reviewer/Linter verification.
