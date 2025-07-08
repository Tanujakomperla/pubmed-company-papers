import typer
import pandas as pd
from pubmed_papers.api import search_pubmed, fetch_pubmed_details
from pubmed_papers.parser import parse_articles
from typing import Optional
import sys
import traceback  # ✅ Add this import

app = typer.Typer()

@app.command()
def main(
    query: str,
    max_results: int = 10,
    file: Optional[str] = typer.Option(None, "-f", "--file", help="File to save results as CSV"),
    debug: bool = typer.Option(False, "-d", "--debug", help="Enable debug output")
):
    """
    Fetch research papers from PubMed based on a search query.
    Filters for papers with authors from non-academic pharma/biotech companies.
    """
    try:
        if debug:
            typer.echo(f"🔍 Searching PubMed with query: {query}")

        ids = search_pubmed(query, max_results=max_results)
        if debug:
            typer.echo(f"✅ Found {len(ids)} papers: {ids}")

        raw_articles = fetch_pubmed_details(ids)
        parsed_data = parse_articles(raw_articles)

        df = pd.DataFrame(parsed_data)

        if file:
            df.to_csv(file, index=False)
            typer.echo(f"✅ Results saved to {file}")
        else:
            typer.echo(df.to_string(index=False))

    except Exception as e:
        typer.echo("❌ Error occurred:", err=True)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    app()
