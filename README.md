# Nova Researcher

An independent, cross-disciplinary AI researcher powered by the integration of top-down planning (AI-Researcher) and bottom-up swarm execution (ScienceClaw).

## Architecture
- **PI Agent:** A context-heavy LLM generating hypotheses and synthesizing artifacts into complete papers.
- **Swarm Agents:** Specialized, lightweight tools performing literature retrieval and analysis.
- **Artifact Reactor:** The shared state (DAG) syncing the Swarm's asynchronous results with the PI.

## Quick Start
*See `docs/PRD.md` for architectural concepts.*
