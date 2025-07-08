import requests
import xmltodict
from typing import List, Dict

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search_pubmed(query: str, max_results: int = 10) -> List[str]:
    """
    Search PubMed for a given query and return list of PubMed IDs.
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }
    response = requests.get(f"{BASE_URL}/esearch.fcgi", params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]


def fetch_pubmed_details(pubmed_ids: List[str]) -> List[Dict]:
    """
    Fetch detailed information for a list of PubMed IDs.
    """
    if not pubmed_ids:
        return []

    ids_str = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": ids_str,
        "retmode": "xml",
    }
    response = requests.get(f"{BASE_URL}/efetch.fcgi", params=params)
    response.raise_for_status()
    parsed = xmltodict.parse(response.content)
    return parsed.get("PubmedArticleSet", {}).get("PubmedArticle", [])
