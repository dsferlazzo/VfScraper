from playwright.sync_api import sync_playwright


validStates = ["Successful","Failed", "Stopped", "No Action"]   #LISTA DEGLI STATUS VALIDI DELLA PIPELINE
pipelineStatusDict = {}
with sync_playwright() as p:
    # Carica lo stato salvato
    browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe", headless=False)  # headless=False = mostra il browser
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.set_viewport_size({"width": 1600, "height": 1200})
    page.goto("https://app.eu.visualfabriq.com/bifrost/nttdata/pipelines")

    posX = 246
    posXStart = posX
    posY = 243

    page.wait_for_timeout(7000)

    while(True):
        posX = posX +5
        page.mouse.move(posX, posY)

        # Trova l'elemento sotto il cursore
        element_class = page.evaluate("""
                ([x, y]) => {
                    const el = document.elementFromPoint(x, y);
                    return el ? el.className : null;
                }
            """, [posX, posY])

        if element_class and "bifrostcss-hBAxAh" in element_class.split():
            print("✅ Il mouse è sopra un elemento della classe 'bifrostcss-hBAxAh'")
            print("Offset " + str(posX - posXStart))
            break
        else:
            print("❌ No, il mouse non è sopra quell'elemento")

    page.wait_for_timeout(4000)
    page.screenshot()
    browser.close()

