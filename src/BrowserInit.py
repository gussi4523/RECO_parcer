


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

    #options = Options()

    # Set the user data directory (this points to the whole Chrome user data folder)
    #options.add_argument(f"--user-data-dir={user_data_dir}")
    #options.add_argument("--profile-directory=SeleniumProfile")
    #service = Service(ChromeDriverManager().install())
    #chrome_options.add_argument("--no-first-run")
    #chrome_options.add_argument("--no-default-browser-check")
    #chrome_options.add_argument("--disable-features=ChromeWhatsNewUI")
    #driver = webdriver.Chrome(service=service,options=options)
    return 1

def CreatePage(p,PROFILE_PATH):
    browser = p.chromium.launch_persistent_context(PROFILE_PATH,headless=False)  # Use headless=True to hide browser
    page = browser.new_page()
    page.goto("https://registrantsearch.reco.on.ca/")
    return page
