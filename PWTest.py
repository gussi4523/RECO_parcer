from src.NotionRESTAPI.NotionRestApi import test
from src.BrowserInit import CreateBrowser
from src.RandomCity.RandomCitySelect import selectRandomCity

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re
import time

from src.NotionRESTAPI.NotionRestApi import createCompanyPageOnNotion, compareExistedPages, createPartnerPageOnNotion, updatePartnerPages, updateCompanyPages, getPageByName

def enterRegistrantSearch(city, driver):
    wait = WebDriverWait(driver, 15)

    # Go to the page
    driver.get("https://registrantsearch.reco.on.ca/")

    # Wait and click category dropdown
    wait.until(EC.element_to_be_clickable((By.ID, "btnCategory"))).click()

    # Wait and select category
    wait.until(EC.presence_of_element_located((By.ID, "dropdownCategory")))
    dropdown = driver.find_element(By.ID, "dropdownCategory")
    for option in dropdown.find_elements(By.TAG_NAME, 'option'):
        if option.get_attribute('value') == "Brokerage/Branch":
            option.click()
            break

    # Wait and fill city
    city_input = wait.until(EC.element_to_be_clickable((By.ID, "categoryCity")))
    city_input.clear()
    city_input.send_keys(city)

    # Click search
    wait.until(EC.element_to_be_clickable((By.ID, "searchCategory"))).click()

    # Optional: wait for table or result elements to appear
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mat-row")))

    print("Page title:", driver.title)

def getDataFromPAGE(driver, url):
    def enterWebsiteEmpos(i):
        try:
            heading = driver.find_element(By.ID, f"heading{i}")
            ActionChains(driver).move_to_element(heading).perform()
            heading.click()
    
            time.sleep(1)  # wait for collapse animation
    
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            collapse = soup.find("div", {"id": f"collapse{i}"})
            if not collapse:
                print(f"❌ Collapse {i} not found.")
                return False
    
            # Corrected: find <p> with <strong> containing 'Employee List:'
            p = None
            for tag in collapse.find_all("p"):
                strong = tag.find("strong")
                if strong and "Employee List:" in strong.get_text():
                    p = tag
                    break
                
            if not p:
                print(f"❌ No 'Employee List' found for collapse {i}, skipping...")
                return False
    
            time.sleep(1)
    
            # Try to click the <a> inside that <p>
            try:
                p_element = driver.find_element(
                    By.XPATH,
                    f"//div[@id='collapse{i}']//p[strong[contains(text(),'Employee List:')]]/a"
                )
                p_element.click()
                time.sleep(1)
            except Exception as e:
                print("⚠️ Couldn't click employee link:", e)
                return False
    
            return True
        except Exception as e:
            print(f"Error in enterWebsiteEmpos: {e}")
            return False

    def getEmpoes(i):
        def getCards(div):
            fields = {
                "Legal Name": None,
                "The Registrant Position": None,
                "Registration": None,
                "Registration Expiry": None,
            }

            for p in div.find_all("p"):
                strong = p.find("strong")
                if not strong:
                    continue
                label = strong.get_text(strip=True).strip(":")
                strong.extract()
                value = p.get_text(strip=True)
                if label in fields:
                    fields[label] = value

            return fields

        id_list = []
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        collapse_divs = soup.find_all("div", id=re.compile(r"^collapse\d+$"))

        for div in collapse_divs:
            field = getCards(div)
            print(field)
            new_page_id = createPartnerPageOnNotion(Name=field["Legal Name"],
                                                    Position=field["The Registrant Position"],
                                                    Email=None, Phone=None)
            id_list.append({"id": new_page_id})
        return id_list

    def extract_fields(div):
        fields = {
            "Legal Name emps": None,
            "Registration Category": None,
            "Registration Status": None,
            "Registration Expiry": None,
            "Brokerage Name": None,
            "Brokerage Address": None,
            "Brokerage Email": None,
            "Brokerage Phone": None,
            "Brokerage Fax": None,
        }

        for p in div.find_all("p"):
            strong = p.find("strong")
            text = p.get_text(strip=True)
            #print(text)
            if strong:
                label = strong.get_text(strip=True).rstrip(":").strip()
                #print(f"Label : {label}")
                value = text.replace(label, '').strip().lstrip(':').strip()
                #print (f"Value : {value}")
                fields[label] = value
                #if value:
                #    value = value.strip().lstrip(":").strip()
                #    if value.startswith("."):
                #        value = value[1:].strip()
                #    if label in fields:
                #        fields[label] = value
                #        print(f"Fields label : {fields[label]}")
        #print(fields)
        time.sleep(1)
        return fields

    # Scroll down to load content
    for _ in range(10):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(0.3)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Find all elements with id like "collapse0", "collapse1", etc.
    collapse_divs = soup.find_all("div", id=re.compile(r"^collapse\d+$"))
    print(len(collapse_divs))
    time.sleep(1)
    amount = 1
    for i, div in enumerate(collapse_divs):
        print(f"\n=== Collapse {i+1} ===")
        data = extract_fields(div)

        legal_name = data["Legal Name"]
        registration_category = data["Registration Category"]
        registration_status = data["Registration Status"]
        registration_expiry = data["Registration Expiry"]
        brokerage_name = data["Brokerage Name"]
        brokerage_address = data["Brokerage Address"]
        brokerage_email = data["Brokerage Email"]
        brokerage_phone = data["Brokerage Phone"]
        brokerage_fax = data["Brokerage Fax"]

        print(legal_name)
        print(brokerage_email)
        print(brokerage_phone)
        print(brokerage_fax)
        print(brokerage_address)
        print(brokerage_name)
        print(registration_expiry)
        print(registration_status)
        print(registration_category)

        EmposId = []
        try:
            success = enterWebsiteEmpos(i)
            print("Employee list success:", success)

            if success:
                try:
                    EmposId = getEmpoes(i)
                except Exception as e:
                    print("Empos not extracted:", e)

                driver.back()
                time.sleep(1)
            else:
                raise ValueError("No employees found")
        except Exception as e:
            print("No employee link exists:", e)
            EmposId.append({"id": createPartnerPageOnNotion(Name=legal_name, Position=None, Email=brokerage_email, Phone=brokerage_phone)})
            print("👨‍💼 Single employee added")

        if not compareExistedPages(legal_name):
            CompanyId = createCompanyPageOnNotion(Name=legal_name, Address=brokerage_address, Phone=brokerage_phone, Email=brokerage_email)
            amount += 1
            if success:
                updatePartnerPages(pageId=EmposId, CompanyId=CompanyId)
                updateCompanyPages(pageId=CompanyId, EmployesId=EmposId)
        else:
            page_id = getPageByName(legal_name, True)
            updateCompanyPages(page_id, EmposId)
            updatePartnerPages(pageId=EmposId, CompanyId=page_id)

        print(f"{amount-1} companies added")

driver = CreateBrowser()
enterRegistrantSearch(city=selectRandomCity("./data/ontarioCities.json"),driver=driver)
getDataFromPAGE(driver=driver,url="./data/txt")