import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from notion_client import Client
import time
from dotenv import load_dotenv
import os

load_dotenv


# Notion setup
NOTION_TOKEN = os.getenv("NOTION_API_KEY") # or paste your "secret_xxx"
DATABASE_ID = "30cf3019db6e4c2aa529c31a976b6809"

notion = Client(auth=NOTION_TOKEN)
ID = notion.users.me()["id"]

def fetch_pages(batch_size=100):
    """Fetch up to batch_size pages created by this user"""
    response = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "and":[{
                    "property": "Created by",
                "created_by": {"contains": ID}
                },{
                    "property": "CompanyName",
                    "relation":{"is_empty": True}
                }]
                
            },
            "page_size": batch_size
        }
    )
    return response["results"]


def archive_page(page_id: str):
    """Archive a Notion page safely"""
    try:
        notion.pages.update(page_id=page_id, archived=True)
        return f"✅ Archived {page_id}"
    except Exception as e:
        return f"❌ Failed {page_id}: {e}"


def main():
    while True:
        pages = fetch_pages(batch_size=100)
        if not pages:
            print("No more pages to delete. Exiting.")
            break

        print(f"Found {len(pages)} pages to archive...")

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(archive_page, page["id"]) for page in pages]
            for future in as_completed(futures):
                print(future.result())

        # Optional: short delay to avoid hitting Notion rate limits
        time.sleep(1)


if __name__ == "__main__":
    main()