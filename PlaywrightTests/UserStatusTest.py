from playwright.sync_api import sync_playwright

# Listener per catturare le response
def handle_response(response):
    if response.url == "https://app.visualfabriq.com/api/user/list":
        print("URL:", response.url)
        print("Status:", response.status)
        try:
            # Prova a leggere il corpo della response come testo
            print("Body:", response.text())     #stampo il response
        except Exception as e:
            print("Non è stato possibile leggere il body:", e)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
                                headless=False)  # headless=False = mostra il browser
    context = browser.new_context(storage_state="state.json", device_scale_factor=1)
    page = context.new_page()
    page.on("response", handle_response)
    page.goto("https://app.eu.visualfabriq.com/configuration/user-and-access/user")


    # Aspetta un po' se ci sono richieste in background
    page.wait_for_timeout(5000)

    browser.close()