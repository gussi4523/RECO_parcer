
from src.DATAScrapper.recoParse import enterRegistrantSearch  ,getDataFromPAGE
from src.BrowserInit import CreateBrowser , CreatePage
import time
from playwright.sync_api import sync_playwright
from src.RandomCity.RandomCitySelect import selectRandomCity,getListOfCities
import random

cities = getListOfCities("./data/ontarioCities.json")

with sync_playwright() as p:
    print(len(cities))
    while len(cities) > 0 :
        r=random.randint(0,len(cities))
        #driver = CreateBrowser()
        page = CreatePage(p,PROFILE_PATH="./data/profile")
        enterRegistrantSearch(cities[r],page=page)
        getDataFromPAGE(page=page,url="./data/txt")
        cities.pop(r)
        print(len(cities))
    
