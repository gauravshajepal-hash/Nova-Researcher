import requests
import time

class DeepResearchSkill:
    """Explodes a single need into orthogonal sub-queries across literature."""
    
    def __init__(self):
        self.base_url = "https://api.openalex.org/works"

    def execute(self, need_context: dict) -> str:
        topic = need_context.get("topic", "")
        
        # Step 1: Query Expansion
        sub_queries = [
            f"{topic}",
            f"{topic} AND (review OR meta-analysis)",
            f"{topic} AND mechanisms",
            f"{topic} AND (applications OR future models)"
        ]
        
        compiled_findings = f"# Deep Research Synthesis: {topic}\n\n"
        compiled_findings += f"**Methodology**: Dynamically expanded the base query into {len(sub_queries)} orthogonal sub-queries to map the full knowledge graph.\n\n"
        
        # Step 2: Iterative Retrieval
        for query in sub_queries:
            try:
                params = {"search": query, "per-page": 3, "sort": "cited_by_count:desc"}
                response = requests.get(self.base_url, params=params, timeout=10)
                data = response.json()
                
                compiled_findings += f"### Sub-Query Synthesis: `{query}`\n"
                if "results" in data:
                    for work in data["results"]:
                        title = work.get("title", "Untitled")
                        doi = work.get("doi", "No DOI")
                        abstract = work.get("abstract_inverted_index", {})
                        
                        # Step 3: Context Compression
                        abstract_text = self._reconstruct_abstract(abstract)
                        compressed = abstract_text[:400] + "... [TRUNCATED FOR CONTEXT COMPRESSION]" if len(abstract_text) > 400 else abstract_text
                        compiled_findings += f"- **{title}** ({doi}): {compressed}\n"
                
                compiled_findings += "\n"
                # Avoid rate limits
                time.sleep(1)
            except Exception as e:
                compiled_findings += f"- [Error retrieving sub-query '{query}']: {e}\n"

        return compiled_findings

    def _reconstruct_abstract(self, inverted_index: dict) -> str:
        if not inverted_index:
            return "No abstract available."
        
        try:
            word_index = []
            for word, positions in inverted_index.items():
                for pos in positions:
                    word_index.append((pos, word))
            word_index.sort()
            return " ".join([word for _, word in word_index])
        except Exception:
            return "Abstract metadata parsing failed."
