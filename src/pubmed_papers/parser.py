from typing import List, Dict
import re

# Define keywords to detect non-academic affiliations
NON_ACADEMIC_KEYWORDS = [
    "pharma", "biotech", "therapeutics", "laboratories", "inc", "ltd",
    "corp", "company", "technologies", "genomics", "biosciences"
]

ACADEMIC_KEYWORDS = [
    "university", "institute", "college", "school", "department", "hospital", "center", "centre"
]


def is_non_academic(affiliation: str) -> bool:
    affiliation_lower = affiliation.lower()
    if any(word in affiliation_lower for word in ACADEMIC_KEYWORDS):
        return False
    return any(word in affiliation_lower for word in NON_ACADEMIC_KEYWORDS)


def parse_pubmed_article(article: Dict) -> Dict:
    """
    Extract required info from a single PubMed article.
    """
    article_data = {}

    # PubMed ID
    article_data["PubmedID"] = article.get("MedlineCitation", {}).get("PMID", "#N/A")

    # Title
    article_data["Title"] = article.get("MedlineCitation", {}).get("Article", {}).get("ArticleTitle", "#N/A")

    # Publication Date
    pub_date = article.get("MedlineCitation", {}).get("Article", {}).get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
    year = pub_date.get("Year", "")
    month = pub_date.get("Month", "")
    day = pub_date.get("Day", "")
    article_data["Publication Date"] = f"{year}-{month}-{day}".strip("-")

    # Authors
    authors = article.get("MedlineCitation", {}).get("Article", {}).get("AuthorList", {}).get("Author", [])
    if not isinstance(authors, list):
        authors = [authors]

    non_academic_authors = []
    company_affiliations = []
    corresponding_email = ""

    for author in authors:
        affiliation_info = author.get("AffiliationInfo")
        if affiliation_info:
            # Safe handling for both list and dict
            if isinstance(affiliation_info, list):
                affiliation = affiliation_info[0].get("Affiliation", "")
            elif isinstance(affiliation_info, dict):
                affiliation = affiliation_info.get("Affiliation", "")
            else:
                affiliation = ""

            # Check if non-academic
            if is_non_academic(affiliation):
                name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
                non_academic_authors.append(name)
                company_affiliations.append(affiliation)

            # Extract email
            email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", affiliation)
            if email_match:
                corresponding_email = email_match.group()

    article_data["Non-academic Author(s)"] = "; ".join(non_academic_authors) if non_academic_authors else "N/A"
    article_data["Company Affiliation(s)"] = "; ".join(company_affiliations) if company_affiliations else "N/A"
    article_data["Corresponding Author Email"] = corresponding_email if corresponding_email else "N/A"

    return article_data


def parse_articles(articles: List[Dict]) -> List[Dict]:
    return [parse_pubmed_article(article) for article in articles]
