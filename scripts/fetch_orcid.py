import requests
import yaml

ORCID_ID = "0000-0002-7470-177X"

url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"

headers = {
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

data = response.json()

works = []

for group in data["group"]:
    summary = group["work-summary"][0]

    title = summary["title"]["title"]["value"]

    year = ""

    if summary.get("publication-date"):
        year = summary["publication-date"]["year"]["value"]

    works.append({
        "title": title,
        "year": year
    })


# nejnovější první
works = sorted(
    works,
    key=lambda x: x["year"],
    reverse=True
)


with open("_data/publications.yml", "w", encoding="utf-8") as f:
    yaml.dump(
        works,
        f,
        allow_unicode=True,
        sort_keys=False
    )

print("Publications updated.")
