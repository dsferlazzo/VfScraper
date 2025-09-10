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
    page.mouse.click(670,144)
    page.wait_for_timeout(500)
    page.mouse.click(680, 251)
    page.wait_for_timeout(500)
    page.mouse.click(1030, 143)
    page.wait_for_timeout(500)
    page.mouse.click(986, 185)
    page.wait_for_timeout(500)
    page.mouse.click(1545, 368)  #ESCO DALLA SCHERMATA DEL FILTRO

    page.wait_for_timeout(1000)

    page.screenshot(path="screenshot.png")
    browser.close()
