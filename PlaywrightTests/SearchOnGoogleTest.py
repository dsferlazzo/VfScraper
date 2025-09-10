from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe", headless=False)  # headless=False = mostra il browser
    page = browser.new_page()
    page.goto("https://www.google.com")


    try:    #PER CHIUDERE IL PULSANTE DEI COOKIE
        page.click("button:has-text('Accetta tutto')", timeout=3000)
    except:
        print("Nessun popup cookie trovato")

    # Scrivi "Playwright automation" nella textbox
    page.fill('textarea[name="q"]', "Playwright automation")

    # Premi Enter
    page.press('textarea[name="q"]', "Enter")

    # Aspetta un paio di secondi per vedere i risultati
    page.wait_for_timeout(5000)

    # Screenshot della pagina
    page.screenshot(path="screenshot.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
