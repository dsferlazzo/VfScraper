from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Carica lo stato salvato
    browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe", headless=False)  # headless=False = mostra il browser
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.set_viewport_size({"width": 1600, "height": 1200})
    page.goto("https://app.eu.visualfabriq.com/bifrost/nttdata/pipelines")

    #CLICCO SUL PULSANTE DEI FILTRI
    page.click("text=Filters")

    #APPLICO IL FILTRO 'Pipeline Status' = 'True'
    page.wait_for_timeout(500)
    page.locator(".bifrostcss-JgNqY").nth(2).click() #CLICCO SUL PULSANTE DI SELEZIONE TIPO DI FILTRO
    page.wait_for_timeout(500)
    page.locator(".bifrostcss-eGauau").nth(2).click()   #CLICCO SUL TIPO DI FILTRO (Pipeline Status)
    page.wait_for_timeout(500)
    page.locator(".bifrostcss-JgNqY").nth(3).click()    #CLICCO SULLA SBARRA DI SELEZIONE STATO
    page.wait_for_timeout(500)
    page.locator(".bifrostcss-eGauau").nth(0).click()     #SELEZIONO LO STATO Enabled
    page.wait_for_timeout(500)
    page.click("text=Apply")  # APPLICO IL FILTRO SELEZIONATO

    page.wait_for_timeout(5000)

    page.screenshot(path="screenshot.png")
    browser.close()
