from playwright.sync_api import sync_playwright

def getStatusPos(box):  #PARTENDO DALLA BOX DEL NOME DELLA PIPELINE, OTTIENE LA POSIZIONE DELL'ULTIMO ESITO DELLA PIPELINE
    center_x = box["x"] + box["width"] / 2
    center_y = box["y"] + box["height"] / 2
    return center_x + 366, center_y

with sync_playwright() as p:
    # Carica lo stato salvato
    browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe", headless=False)  # headless=False = mostra il browser
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.goto("https://app.eu.visualfabriq.com/bifrost/nttdata/pipelines")

    page.wait_for_timeout(7000)
    posX, posY = 542, 247   #LA POSIZIONE IN PIXEL DELL'ESITO DELLA PIPELINE

    page.mouse.move(posX, posY)
    page.wait_for_timeout(500)

    page.mouse.dblclick(posX, posY - 43)

    selected_text = page.evaluate("window.getSelection().toString()")
    print("Testo selezionato:", selected_text)

    page.screenshot(path="screenshot.png")  #DEBUGGING
    browser.close()

