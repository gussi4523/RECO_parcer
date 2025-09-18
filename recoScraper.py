
from src.DATAScrapper.recoParse import enterRegistrantSearch  ,getDataFromPAGE
from src.BrowserInit import CreateBrowser , CreatePage
import time
#from playwright.sync_api import sync_playwright
from src.RandomCity.RandomCitySelect import selectRandomCity, getListOfCities
import random
import os 
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

## Create persistent browser context onc
#while len(cities) > 0 :
#    enterRegistrantSearch(city=selectRandomCity(f"{scriptURL}/data/ontarioCities.json"),driver=driver)
#    getDataFromPAGE(driver=driver,url="./data/txt")

driver = CreateBrowser()
scriptURL = os.path.dirname(os.path.abspath(__file__))

while True:  # infinite loop
    cities = getListOfCities("./data/ontarioCities.json")  # load cities
    #print(len(cities))
    random.shuffle(cities)  # shuffle to process in random order
    print(len(cities))
    for city in cities:
        enterRegistrantSearch(city=city, driver=driver)
        getDataFromPAGE(driver=driver, url="./data/txt")
        time.sleep(0.5)  # optional: avoid overwhelming the site
    
