from dotenv import load_dotenv
import os
from notion_client import Client

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY") 
DATABASE_ID  = os.getenv("DATABASE_ID")
DATABASE_ID_P  = os.getenv("DATABASE_ID_P")

notion = Client(auth=NOTION_API_KEY)

# === Add this near your other config ===
PROJECTS_DB_ID = "48c93139d07f46778fe93be9298c8afd"  # NOT a page id; the DB id of your Projects database
PROJECT_TITLE_PROP = "Name"                    # title prop in Projects DB (change if yours differs)

results = []
has_more = True
cursor = None

while has_more:
    response = notion.databases.query(
        **{
            "database_id": PROJECTS_DB_ID,
            "start_cursor": cursor,
            "page_size": 100  # max allowed
        }
    )

    results.extend(response["results"])

    has_more = response["has_more"]
    cursor = response.get("next_cursor")

print(f"Total pages fetched: {len(results)}")
for page in results:
    page_id = page["id"]
    # The title property is usually called "Name"
    title_property = page["properties"]["Name"]["title"]
    name = "".join([t["plain_text"] for t in title_property])
    print(f"{page_id} - {name}")

