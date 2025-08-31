
#--- Delete created by API
from notion_client import Client
from dotenv import load_dotenv
import os
import json
from src.UniqueCodeGEN.uniquecodeGenerator import generateUniquecode
from notion_client.errors import APIResponseError
from concurrent.futures import ThreadPoolExecutor

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY") 
DATABASE_ID  = os.getenv("DATABASE_ID")
DATABASE_ID_P  = os.getenv("DATABASE_ID_P")

notion = Client(auth=NOTION_API_KEY)

db = notion.databases.retrieve(database_id=DATABASE_ID)
print(json.dumps(db,indent=2,ensure_ascii=False))

all_pages = []
next_cursor = None

# Fetch pages created by USER_ID
while True:
    response = notion.databases.query(
        database_id=DATABASE_ID,
        page_size=100,
        start_cursor=next_cursor,
        filter={
            "property": "Created by",
            "created_by": {
                "contains": "3775d289-6cc2-4775-85f2-94dfc388b384"  # must use "contains"
            }
        }
    )

    all_pages.extend(response["results"])

    if response.get("has_more"):
        next_cursor = response["next_cursor"]
        print("Fetched next 100 pages, total so far:", len(all_pages))
    else:
        break

# Function to delete a page
def delete_page(page):
    title_prop = page["properties"]["BrokerageName"]["title"]
    title_text = title_prop[0]["text"]["content"] if title_prop else "No title"
    notion.pages.update(page_id=page["id"], archived=True)
    print(title_text + " deleted")

# Delete pages concurrently for speed
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(delete_page, all_pages)