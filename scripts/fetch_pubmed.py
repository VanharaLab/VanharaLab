from pathlib import Path

import requests
import yaml
import xml.etree.ElementTree as ET


AUTHOR_QUERY = "Vanhara P[Author]"

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


# Najít PMID
params = {
    "db": "pubmed",
    "term": AUTHOR_QUERY,
    "retmax": 500,
    "retmode": "json"
}

response = requests.get(ESEARCH_URL, params=params)
response.raise_for_status()

pmids = response.json()["esearchresult"]["idlist"]

print(f"Found {len(pmids)} PubMed records")


if not pmids:
    raise SystemExit("No publications found")


# Stáhnout XML záznamy
params = {
    "db": "pubmed",
    "id": ",".join(pmids),
    "retmode": "xml"
}

response = requests.get(EFETCH_URL, params=params)
response.raise_for_status()

root = ET.fromstring(response.text)


publications = []


for article in root.findall(".//PubmedArticle"):

    art = article.find(".//Article")

    title = art.findtext(
        "ArticleTitle",
        default=""
    )

    journal = art.findtext(
        ".//Journal/Title",
        default=""
    )

    year = art.findtext(
        ".//PubDate/Year",
        default=""
    )

    volume = art.findtext(
        ".//JournalIssue/Volume",
        default=""
    )

    issue = art.findtext(
        ".//JournalIssue/Issue",
        default=""
    )

    pages = art.findtext(
        ".//Pagination/MedlinePgn",
        default=""
    )


    authors = []

    for author in art.findall(".//Author"):
        lastname = author.findtext("LastName")
        initials = author.findtext("Initials")

        if lastname:
            authors.append(
                f"{lastname} {initials or ''}".strip()
            )


    doi = ""

    for aid in article.findall(".//ArticleId"):
        if aid.attrib.get("IdType") == "doi":
            doi = aid.text


    pmid = article.findtext(
        ".//PMID",
        default=""
    )

    print(
        year,
        title,
        journal,
        volume,
        issue,
        pages,
        doi,
        pmid
    )
    
    publications.append(
        {
            "year": year,
            "title": title,
            "authors": ", ".join(authors),
            "journal": journal,
            "volume": volume,
            "issue": issue,
            "pages": pages,
            "doi": doi,
            "pmid": pmid
        }
    )


publications.sort(
    key=lambda x: int(x["year"]) if x["year"] else 0,
    reverse=True
)


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT = BASE_DIR / "_data" / "publications.yml"

print(f"Saving publications to: {OUTPUT}")

with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:
    yaml.dump(
        publications,
        f,
        allow_unicode=True,
        sort_keys=False
    )

print(f"File exists: {OUTPUT.exists()}")
print(f"File size: {OUTPUT.stat().st_size} bytes")

print(
    f"Saved {len(publications)} publications"
)
