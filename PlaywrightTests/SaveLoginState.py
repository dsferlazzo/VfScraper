from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",headless=False)  # headless=False = mostra il browser

    page = browser.new_page()
    page.goto("https://app.eu.visualfabriq.com/dashboard")

    # Qui fai login manualmente (SSO, username, password, ecc.)
    input("Fai login e poi premi Invio...")

    # Salva lo stato di login (cookie + localStorage) in un file
    page.context.storage_state(path="state.json")
    browser.close()
