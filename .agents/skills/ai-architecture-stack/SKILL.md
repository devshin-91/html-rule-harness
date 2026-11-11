---
name: ai-architecture-stack
description: Select and compose Prompt, Context, Harness, Loop, and Graph engineering techniques (and multi-technique combinations) for AI system design and complex agentic use cases. Use when designing AI pipelines, RAG/memory layers, agent loops, stateful multi-agent graphs, or hybrid combinations.
---

# AI Engineering Stack & Combination Selector

## Five Pillars Decision Matrix
1. **Prompt (`prompt`)**: Use when single-turn clarity, typed JSON schemas, few-shot examples, or prompt chaining solves the problem. Lowest latency/cost.
2. **Context (`context`)**: Use when external knowledge (Hybrid RAG / GraphRAG), multi-session memory (Mem0), compaction, or progressive disclosure prevents context rot.
3. **Harness (`harness`)**: Use when agents touch files/tools/APIs and need sandboxes, Pre/PostToolUse hooks, deterministic validators, or online/offline Evals.
4. **Loop (`loop`)**: Use when verifiable feedback drives quality (ReAct tool loop, Evaluator-Optimizer, test-gated retry, Reflexion).
5. **Graph (`graph`)**: Use when workflows need cyclic state machines, Fan-out/Fan-in parallelism, Orchestrator-Workers, durable checkpointing, or Human-in-the-Loop (LangGraph / ADK Workflow / Pydantic Graph).

## High-Value Combination Recipes
- **Prompt + Context**: Typed structured extraction grounded in Hybrid RAG / entity memory.
- **Context + Loop**: Corrective RAG / Agentic retrieval loop with query reformulation and context compaction.
- **Harness + Loop**: Verifier-gated coding/execution loop (linter/unit-test backpressure + Propose–Probe–Compose).
- **Graph + Harness + Context**: Long-running stateful multi-agent graph with per-node context isolation, model-tier routing, and durable checkpoints.
