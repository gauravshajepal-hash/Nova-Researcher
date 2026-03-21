# Workspace Memory: Nova Researcher

- **Stack:** Python 3.11+, LiteLLM, Pydantic (for structured Artifacts).
- **Core Principle:** Cross-disciplinary discovery (Physics -> Population Science).
- **Key Mechanism:** The ArtifactReactor acts as an asynchronous DAG. Swarm never blocks. If an API fails or a PDF is paywalled, it sets a "human_pdf_retrieval" Unmet Need and processes the metadata/abstract instead.
- **APIs:** OpenAlex, arXiv, Crossref. No Semantic Scholar.
