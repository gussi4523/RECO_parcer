from notion_client import Client
import json
from dotenv import load_dotenv
import os
from src.UniqueCodeGEN.uniquecodeGenerator import generateUniquecode

# --- Configuration ---
# It's best practice to store sensitive keys in environment variables
# For a quick start, you can paste them directly, but REMOVE them for production!
# Option 1: Direct pasting (less secure, good for quick testing)
load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY") 
DATABASE_ID  = os.getenv("DATABASE_ID")
DATABASE_ID_P  = os.getenv("DATABASE_ID_P")

notion = Client(auth=NOTION_API_KEY)

db = notion.databases.retrieve(database_id=DATABASE_ID)

print(json.dumps(db,indent=2,ensure_ascii=False))

# --- CREATE FUNCTION ---
def createCompanyPageOnNotion(Name, Address,Phone,Email):
    new_page = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "BrokerageName": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": Name
                        }
                    }
                ]
            },
            "BrokerageAddress":{
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": Address if Address else None  # змінна або рядок
                        }
                    }
                ]
            },
            "BrokeragePhone":{
                "phone_number": Phone if Phone else None
            },
            "BrokerageEmail":{
                "email": Email if Email else None
            },
            "Status":{
                "status":{
                    "name":"Not started"
                }
            },
        },
        icon={
            "type": "external",
            "external": {
                "url": "https://www.notion.so/icons/shop_red.svg"
            }
        }
    )
    print(new_page["id"])
    return new_page["id"]

def updateCompanyPages(pageId:str,EmployesId: list[dict[str,str]]):
    notion.pages.update(
        page_id= pageId,
        properties={
            "BrokerageEmployees":{
                    "relation":[
                    {"id":rid["id"]} for rid in EmployesId
                ]
            }
        }
    )
    print("employees Added")

def updatePartnerPages(pageId:list[dict[str,str]],CompanyId:str):
    
    for pID in pageId:
        print(pageId)
        notion.pages.update(
            page_id= pID["id"],
            properties={
                "CompanyName":{
                    "relation":[
                        {"id":CompanyId}
                    ]
                }
            }
        )
        print("Company added")

def createPartnerPageOnNotion(Name, Position):
    code = generateUniquecode(8)
    print(code)
    print(Position)

    new_page = notion.pages.create(
        parent={"database_id": DATABASE_ID_P},
        properties={
            "LegalName": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": Name
                        }
                    }
                ]
            },
            "UniqueCode":{
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": code # змінна або рядок
                        }
                    }
                ]
            },
            "TheRegistrationPosition":{
                "select":{
                    "name": Position 
                }
            },
            "Status":{
                "select":{
                    "name":"Not contacted"
                }
            },
        },
        icon={
            "type": "external",
            "external": {
                "url": "https://www.notion.so/icons/alien_red.svg"
            }
        }
    )
    print(new_page["id"])
    return new_page["id"]

def test():
    db = notion.databases.retrieve(database_id=DATABASE_ID_P)

    print(json.dumps(db,indent=2,ensure_ascii=False))
    print(getPageByName("The Auto Hubb",True))

def getPageByName(name: str, company: bool) -> str | None:
    dbID = DATABASE_ID if company else DATABASE_ID_P
    nameProp = "BrokerageName" if company else "LegalName"
    
    response = notion.databases.query(
        database_id=dbID,
        filter={
            "property": nameProp,
            "title": {
                "equals": name
            }
        }
    )

    results = response.get("results")
    if results:
        return results[0]["id"]  # return first matching page id
    else:
        return None  # no page found

def compareExistedPages(name):
    response = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "BrokerageName",  # This must match your title property's name
                "title": {
                    "equals": name
                }
            }
        }
    )

        # Check results
    if response["results"]:
        print("❌ Page exists!")
        return True
    else:
        print("✅ Page does NOT exist.")
        return False

#createPageOnNotion(Name="AAAA",Website="https://www.notion.so/213ee1c44e934309bc3f0a82e46edf7b?v=8d507c8f25634cc5a67101184a2bbb48")