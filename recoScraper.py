
from src.DATAScrapper.recoParse import enterRegistrantSearch  ,getDataFromPAGE
from src.BrowserInit import CreateBrowser , CreatePage
import time
from playwright.sync_api import sync_playwright
from src.RandomCity.RandomCitySelect import selectRandomCity

with sync_playwright() as p:
    #driver = CreateBrowser()
    page = CreatePage(p,PROFILE_PATH="./data/profile")
    enterRegistrantSearch(selectRandomCity("./data/ontarioCities.json"),page=page)
    getDataFromPAGE(page=page,url="./data/txt")
    
