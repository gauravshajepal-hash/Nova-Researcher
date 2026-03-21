# 🚀 Nova Researcher

**Nova Researcher** is a fully autonomous, cross-disciplinary scientific discovery system. It was forged by conceptually merging two paradigm-defining AI research architectures:

1. **[HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher)**
   * **Contribution:** The "Principal Investigator" (PI) model. It provides the top-down methodology for defining research trajectories, conducting literature reviews, algorithm validation, and synthesizing final academic manuscripts.
2. **[lamm-mit/scienceclaw](https://github.com/lamm-mit/scienceclaw)**
   * **Contribution:** The decentralized "Laboratory Swarm" model. Rather than relying on rigid, single-thread scripts, it introduces the **ArtifactReactor**—an asynchronous event bus (`global_index.jsonl`) where specialized agents broadcast needs and resolve them dynamically.

---

## 🏛️ System Architecture

The Nova Researcher operates on a **Decentralized Event-Driven Graph**:

* **The Principal Investigator (`src/pi_agent/`)**
  * Powered by context-heavy models (e.g., *Gemini 1.5 Pro*, *Claude 3.5 Sonnet*) via **LiteLLM**.
  * The PI does *not* fetch data directly. Instead, it generates a high-level hypothesis (e.g., applying *Active Matter* physics to *Population Science*) and broadcasts targeted **Unmet Needs** (like `"need": "literature_search"`) to the reactor.
  * Once the Swarm completes its experiments, the `PIWriter` ingests the resulting Directed Acyclic Graph (DAG) of completed Artifacts and synthesizes a hallucination-free research paper.

* **The Laboratory Swarm (`src/swarm/`)**
  * Fast, specialized worker nodes running continuously (`BaseAgent`). 
  * They read the `unmet_needs.jsonl` file. When a need matches their skill, they execute (e.g., `LiteratureAgent` searches the open internet).
  * **Keyless Design:** Built-in skills like `LiteratureSkill` use **OpenAlex** and **arXiv** APIs, requiring zero authentication to pull down real-world academic abstracts and DOIs.

* **The Artifact Reactor (`src/reactor/`)**
  * The synchronization engine protecting the `global_index.jsonl` and `unmet_needs.jsonl` with strict `filelock` concurrency. 
  * It guarantees that hundreds of parallel Swarm agents can write their experimental results back to the PI asynchronously without race conditions on Windows/Linux environments.

* **Human-in-the-Loop Eventual Consistency**
  * If the Swarm hits a closed-access paper, it doesn't crash. It writes an abstract-based hypothesis, broadcasts a `human_pdf_retrieval` need to you, and continues working. When you drop the PDF into the system later, it dynamically updates its prior assertions.

---

## ⚙️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/gauravshajepal-hash/Nova-Researcher.git
   cd Nova-Researcher
   ```

2. **Install Dependencies**
   The system relies on LiteLLM for universal API tracking, Pydantic for rigid Swarm state enforcement, and FileLock for safe OS concurrency.
   ```bash
   pip install litellm python-dotenv filelock pydantic requests tenacity
   ```

3. **Configure Environment**
   Because the system uses **LiteLLM**, you are entirely model-agnostic. You can hot-swap Google, OpenAI, Anthropic, or Qwen keys endlessly.
   ```bash
   cp .env.template .env
   # Open .env and insert your preferred model key (e.g., GEMINI_API_KEY=sk-...)
   ```

---

## 🔬 How to Run the Researcher

To watch the emergent intelligence happen, you need to simulate the PI giving orders to the Lab Swarm. Open **two separate terminal windows**:

### Terminal 1: The Swarm Worker
The Swarm workers poll the reactor endlessly, waiting for assignments.
```bash
python -m src.swarm.literature_worker
```
*(Leave this terminal running. It will sit dormant until the PI gives it a task.)*

### Terminal 2: The Principal Investigator
Trigger the high-level orchestrator to begin a research seed.
```bash
python main.py
```
* You will be prompted to enter `Domain A`, `Domain B`, and a `Core Concept`.
* The PI will reach out to your LLM (using the keys in your `.env`).
* It will mathematically derive 3 Sub-Topics for investigation and immediately broadcast those Needs to the Swarm.

### The Emergence
The moment you press Enter in Terminal 2, look at Terminal 1. The Swarm worker will wake up, snag the jobs out of `unmet_needs.jsonl`, blast live requests to OpenAlex/arXiv, and build the academic knowledge graph in `global_index.jsonl`. 

### 🧪 Dry-Run (No LLM Keys Needed)
If you don't have API keys yet, **it still works!** 
Our custom resilience logic in `orchestrator.py` uses `tenacity`. If it detects an `AuthenticationError`, it gracefully abandons the LLM and falls back to a deterministic Mock-PI. It will generate 3 hardcoded needs so you can still watch the Swarm workers fetch live peer-reviewed data from OpenAlex.
