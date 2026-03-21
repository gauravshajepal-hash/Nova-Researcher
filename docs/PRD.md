# Nova Researcher Product Requirements Document (PRD)

## Vision
To build an AI entity that autonomously conducts cross-disciplinary scientific research (e.g., applying physics models to population dynamics).

## Core Mechanisms
1. **Model-Agnostic LLM Routing:** Driven by `LiteLLM` for Universal API support.
2. **Open Data Retrieval:** Utilizing OpenAlex, arXiv, and Crossref instead of relying on closed APIs.
3. **Asynchronous HITL:** Instead of pausing on gated text, agents parse abstracts, draft a hypothesis, and flag humans for the full PDF. Synthesis updates dynamically upon human delivery.

## Core Modules
- `src/pi_agent/`: Orchestrates the `global_index.jsonl`. Subscribes to Swarm DAGs.
- `src/swarm/`: Specialized workers (e.g., `LiteratureAgent`) polling the Artifact Reactor.
- `src/reactor/`: Graph management, artifact storage, and event bus (`ArtifactReactor`).
