from src.NotionRESTAPI.NotionRestApi import getPageByName
id = getPageByName("b",False)
print(id)
if id == None:
    #EmposId.append({"id": createPartnerPageOnNotion(Name=legal_name, Position=None, Email=brokerage_email, Phone=brokerage_phone)})
    print("👨‍💼 Single employee added")