from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

def CreateBrowser():
    # Replace this with your desired command
    powershell_command = (
        'Start-Process "chrome.exe" '
        f'-ArgumentList "--remote-debugging-port=9222", "--start-maximized"'
    )

    # Build the command
    linux_command = [
        "firefox",
        "--start-debugger-server",
        "9222"
    ]

    user_data_dir = r"/home/parhomenko-danyiil/.config/SeleniumProfile"

    options = Options()
    options.add_argument(f"--user-data-dir={"./data/profile"}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Optional: avoid detection by setting user-agent, etc.
    # options.add_argument("user-agent=...")

    # Initialize Chrome driver
    driver = webdriver.Chrome(options=options)

    # Go to the target page
    driver.get("https://registrantsearch.reco.on.ca/")

    return driver

def CreatePage(p,PROFILE_PATH):
    browser = p.chromium.launch_persistent_context(PROFILE_PATH,headless=False)  # Use headless=True to hide browser
    page = browser.new_page()
    page.goto("https://registrantsearch.reco.on.ca/")
    return page
