import requests
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

class LiteratureSkill:
    """Zero-key literature retrieval via OpenAlex and arXiv."""

    @staticmethod
    def search_openalex(query: str, limit: int = 5) -> List[Dict]:
        """Fetch metadata/abstracts from OpenAlex (no key required)."""
        url = f"https://api.openalex.org/works?search={query}&per-page={limit}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                for work in data.get("results", []):
                    results.append({
                        "id": work.get("id"),
                        "title": work.get("display_name"),
                        "authors": [a.get("author", {}).get("display_name") for a in work.get("authorships", [])],
                        "abstract_inverted_index": work.get("abstract_inverted_index"),
                        "doi": work.get("doi"),
                        "publication_year": work.get("publication_year"),
                        "is_open_access": work.get("open_access", {}).get("is_oa", False),
                        "pdf_url": work.get("open_access", {}).get("oa_url")
                    })
                return results
        except Exception:
            return []
        return []

    @staticmethod
    def search_arxiv(query: str, limit: int = 5) -> List[Dict]:
        """Fetch pre-prints from arXiv."""
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={limit}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                results = []
                # Simple XML parsing for arXiv atom feed
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    results.append({
                        "title": entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                        "summary": entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                        "id": entry.find('{http://www.w3.org/2005/Atom}id').text,
                        "pdf_url": entry.find("{http://www.w3.org/2005/Atom}link[@title='pdf']").attrib['href'] if entry.find("{http://www.w3.org/2005/Atom}link[@title='pdf']") is not None else None
                    })
                return results
        except Exception:
            return []
        return []

    @staticmethod
    def reconstruct_abstract(inverted_index: Dict) -> str:
        """Helper to turn OpenAlex abstract index back into text."""
        if not inverted_index:
            return ""
        word_positions = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort()
        return " ".join([w[1] for w in word_positions])
