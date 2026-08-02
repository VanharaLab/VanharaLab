import requests
import yaml


ORCID_ID = "0000-0002-7470-177X"

url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"

headers = {
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()

publications = []

for group in data.get("group", []):

    work = group["work-summary"][0]

    title = (
        work.get("title", {})
        .get("title", {})
        .get("value", "")
    )

    year = ""

    if work.get("publication-date"):
        year = (
            work["publication-date"]
            .get("year", {})
            .get("value", "")
        )

    journal = ""

    if work.get("journal-title"):
        journal = work["journal-title"].get("value", "")

    publications.append(
        {
            "title": title,
            "year": year,
            "journal": journal
        }
    )


# řazení od nejnovějších
publications.sort(
    key=lambda x: int(x["year"]) if x["year"] else 0,
    reverse=True
)


with open("_data/publications.yml", "w", encoding="utf-8") as file:
    yaml.dump(
        publications,
        file,
        allow_unicode=True,
        sort_keys=False
    )


print(f"Updated {len(publications)} publications")
