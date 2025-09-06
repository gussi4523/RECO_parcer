
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
CREATE_BY_ID = os.getenv("CREATED_BY_ID")
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
                "contains": CREATE_BY_ID  # must use "contains"
            }
        }
    )

    all_pages.extend(response["results"])

    if response.get("has_more"):
        next_cursor = response["next_cursor"]
        print("Fetched next 100 pages, total so far:", len(all_pages))
    else:
        break

from concurrent.futures import ThreadPoolExecutor, as_completed

def delete_page(page):
    notion.pages.update(page_id=page["id"], archived=True)
    return page["id"]

with ThreadPoolExecutor(max_workers=20) as executor:  # adjust workers
    futures = [executor.submit(delete_page, p) for p in all_pages]

    for future in as_completed(futures):
        try:
            page_id = future.result()
            print(f"Deleted {page_id}")
        except Exception as e:
            print("Error:", e)
