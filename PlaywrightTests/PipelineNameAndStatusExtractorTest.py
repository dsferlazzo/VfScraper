from playwright.sync_api import sync_playwright
import csv

def getOffset():    #FUNZIONE DA RUNNARE QUANDO CAMBIO PAGINA. PER TROVARE L'OFFSET DELLA BOXò
    pass
def getStatusPos(box):  #PARTENDO DALLA BOX DEL NOME DELLA PIPELINE, OTTIENE LA POSIZIONE DELL'ULTIMO ESITO DELLA PIPELINE
    center_x = box["x"] + box["width"] / 2
    center_y = box["y"] + box["height"] / 2
    return center_x + 442, center_y

def getStatusText(posX, posY):  #DATA LA POSIZIONE DELLO STATUS DELLA PIPELINE, NE OTTIENE IL TESTO DI HOVER, DELL'ESITO DELLA RUN
    page.mouse.move(posX, posY) #SPOSTO IL MOUSE ALLA POSIZIONE DELLO STATUS
    page.wait_for_timeout(500)

    page.mouse.dblclick(posX, posY - 43)    #FACCIO DOPPIO-CLICK SULLA POSIZIONE DELL'HOVER

    selectedText = page.evaluate("window.getSelection().toString()")    #OTTENGO IL TESTO SELEZIONATO
    return selectedText

def saveDictAsCSV(dictToSave, fileName):    #SALVA IL CONTENUTO DEL DIZIONARIO IN UN FILE CSV
    with open(fileName, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        #SCRIVO LE INTESTAZIONI
        writer.writerow(["Pipeline", "Run Status"])

        #INSERISCO I DATI DEL DICT NEL FILE
        for pipeline, status in dictToSave.items():
            writer.writerow([pipeline, status])
        print("File salvato come " + str(fileName))


validStates = ["Successful","Failed", "Stopped", "No Action"]   #LISTA DEGLI STATUS VALIDI DELLA PIPELINE
pipelineStatusDict = {}
with sync_playwright() as p:
    # Carica lo stato salvato
    browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe", headless=False)  # headless=False = mostra il browser
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.set_viewport_size({"width": 1600, "height": 1200})
    page.goto("https://app.eu.visualfabriq.com/bifrost/nttdata/pipelines")

    page.wait_for_timeout(10000)
    page.screenshot(path="screenshot.png")  # DEBUGGING
    while(True):
        elements = page.locator(".bifrostcss-eXwpzm.undefined") #TROVO TUTTI GLI ELEMENTI PIPELINE
        count = elements.count()
        print("Elementi trovati " + str(count))

        for i in range(count):  #ITERO PER GLI ELEMENTI, PER TROVARE IL CENTRO DELLA BOX, LO STATUS DELL'ULTIMA RUN ED IL NOME DELLA PIPELINE
            element = elements.nth(i)
            box = element.bounding_box()
            statusPos = getStatusPos(box)   #OTTENGO LA POSIZIONE DELLO STATUS
            #print("Posizione status: " + str(statusPos))    #DEBUGGING
            statusText = getStatusText(statusPos[0], statusPos[1]).strip()  #OTTENGO IL TESTO DI HOVER DELLO STATUS

            if statusText not in validStates:
                statusText = "Never Executed"

            pipelineName = element.inner_text()
            if pipelineName in pipelineStatusDict:  #SE HO GIA SALVATO LA PIPELINE NEL DICT, LA PAGINA NON E STATA RICARICATA, POICHE IL PULSANTE ERA DISATTIVATO
                break
            print("Pipeline: " + str(pipelineName) + " *** Esito: " + str(statusText.strip()))  #DEBUGGING
            pipelineStatusDict[pipelineName] = statusText   #SALVO ALL'INTERNO DI UN DIZIONARIO, PER INSERIRLO SUCCESSIVAMENTE NEL FILE CSV DI OUTPUT

        page.click("text=Next")
        page.wait_for_timeout(4000) #ASPETTO IL CARICAMENTO DELLA NUOVA PAGINA

    saveDictAsCSV(pipelineStatusDict, "pipelineStatusDict.csv")
    page.wait_for_timeout(4000)

    browser.close()

