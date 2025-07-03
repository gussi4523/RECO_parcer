
from src.DATAScrapper.recoParse import enterRegistrantSearch  ,getDataFromPAGE
from src.BrowserInit import CreateBrowser , CreatePage
import time
from playwright.sync_api import sync_playwright
from src.RandomCity.RandomCitySelect import selectRandomCity, getListOfCities
import random

cities = getListOfCities("./data/ontarioCities.json")

#with sync_playwright() as p:
#    print(len(cities))
#    # Create persistent browser context once
#    context = p.chromium.launch_persistent_context(
#        user_data_dir="./data/profile", headless=False
#    )
#    while len(cities) > 0 :
#        r=random.randint(0,len(cities)-1)
#        #driver = CreateBrowser()
#        page = CreatePage(p,PROFILE_PATH="./data/profile")
#        enterRegistrantSearch(cities[r],page=page)
#        getDataFromPAGE(page=page,url="./data/txt")
#        cities.pop(r)
#        print(len(cities))
#    context.close()
    

driver = CreateBrowser()
enterRegistrantSearch(city=selectRandomCity("./data/ontarioCities.json"),driver=driver)
getDataFromPAGE(driver=driver,url="./data/txt")
