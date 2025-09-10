from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Carica lo stato salvato
    browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe", headless=False)  # headless=False = mostra il browser
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.goto("https://app.eu.visualfabriq.com/bifrost/nttdata/pipelines")

    #CLICCO SUL PULSANTE DEI FILTRI
    page.click("text=Filters")

    #APPLICO IL FILTRO 'Pipeline Status' = 'True'
    page.wait_for_timeout(500)
    page.mouse.click(375,144)
    page.wait_for_timeout(500)
    page.mouse.click(356, 251)
    page.wait_for_timeout(500)
    page.mouse.click(690, 143)
    page.wait_for_timeout(500)
    page.mouse.click(668, 187)
    page.wait_for_timeout(500)
    page.mouse.click(1009, 227)  #ESCO DALLA SCHERMATA DEL FILTRO
    '''
    while (page.get_by_text("Next").is_enabled()):
        page.click("text=Next")
        page.wait_for_timeout(1000)
    '''
    page.wait_for_timeout(4000)

    page.screenshot(path="screenshot.png")
    browser.close()
