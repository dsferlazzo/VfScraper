from playwright.sync_api import sync_playwright
import csv

def getStatusBoxPosX():    #FUNZIONE DA RUNNARE QUANDO CAMBIO PAGINA. PER TROVARE LA PosX DELLE BOX
    xPosArray = []
    for bifrostClass in validBifrostClasses:
        elements = page.locator(bifrostClass)  # TROVO TUTTI GLI ELEMENTI PIPELINE
        ct = elements.count()
        if ct != 0:
            element = elements.nth(0)
            box = element.bounding_box()
            centerX = box["x"] + (box["width"] / 2)
            xPosArray.append(centerX)

    if len(xPosArray)==0:   #PER GESTIRE PAGINE SENZA ESECUZIONI
        return 0
    return min(xPosArray)


def getStatusBoxPosY(box): #DATA UNA BOX, RITORNA LA PosY CENTRALE DELLA BOX
    center_y = box["y"] + box["height"] / 2
    return center_y

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

def filterStatusEnabled():  #FUNZIONE CHE FILTRA LE PIPELINE PER Pipeline Status = Enabled
    # CLICCO SUL PULSANTE DEI FILTRI
    page.click("text=Filters")

    # APPLICO IL FILTRO 'Pipeline Status' = 'True'
    page.wait_for_timeout(500)
    page.mouse.click(670, 144)
    page.wait_for_timeout(500)
    page.mouse.click(680, 251)
    page.wait_for_timeout(500)
    page.mouse.click(1030, 143)
    page.wait_for_timeout(500)
    page.mouse.click(986, 185)
    page.wait_for_timeout(500)
    page.mouse.click(1545, 368)  # ESCO DALLA SCHERMATA DEL FILTRO

    page.wait_for_timeout(1000)


validBifrostClasses = [".bifrostcss-hBAxAh",".bifrostcss-dSdRKl",".bifrostcss-fuPzxl"]    #LISTA DI TUTTE LE CLASSI HTML DEGLI STATI DI BIFROST
validStatuses = ["Successful","Failed", "Stopped", "No Action"]   #LISTA DEGLI STATUS VALIDI DELLA PIPELINE
pipelineStatusDict = {}
with sync_playwright() as p:
    # Carica lo stato salvato
    browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe", headless=False)  # headless=False = mostra il browser
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.set_viewport_size({"width": 1600, "height": 1200})
    page.goto("https://app.eu.visualfabriq.com/bifrost/nttdata/pipelines")

    page.wait_for_timeout(10000)
    #filterStatusEnabled()
    exitLoop = False    #FLAG PER USCIRE DAL WHILE LOOP
    while(not exitLoop):
        elements = page.locator(".bifrostcss-eXwpzm.undefined") #TROVO TUTTI GLI ELEMENTI PIPELINE

        firstPipelineName = elements.nth(0).inner_text()    #CONTROLLO SUBITO SE IL PRIMO NOME DELLA PIPELINE E PRESENTE NEL DICT, PER VEDERE SE STO SEMPRE NELLA STESSA PAGINA O SE NE E STATA CARICATA UNA NUOVA
        if firstPipelineName in pipelineStatusDict:  # SE HO GIA SALVATO LA PIPELINE NEL DICT, LA PAGINA NON E STATA RICARICATA, POICHE IL PULSANTE ERA DISATTIVATO
            exitLoop = True
            break

        count = elements.count()
        print("Elementi trovati " + str(count)) #DEBUGGING

        statusPosX = getStatusBoxPosX() #SALVO DOPO IL CARICAMENTO DELLA PAGINA LA PosX DEI PIPELINE STATUS
        if statusPosX == 0: #S
            continue

        for i in range(count):  #ITERO PER GLI ELEMENTI, PER TROVARE IL CENTRO DELLA BOX, LO STATUS DELL'ULTIMA RUN E IL NOME DELLA PIPELINE
            element = elements.nth(i)
            if statusPosX == 0: #GESTISCO SE LA PAGINA NON HA NESSUNA PIPELINE CHE E STATA GIA RUNNATA
                statusText = "Never Executed"
            else:
                box = element.bounding_box()
                statusPos = [statusPosX, getStatusBoxPosY(box)]
                statusText = getStatusText(statusPos[0], statusPos[1]).strip()  #OTTENGO IL TESTO DI HOVER DELLO STATUS

            if statusText == "Action":  #PER GESTIRE IL FATTO CHE IL SISTEMA NON RIESCE A EVIDENZIARE DUE PAROLE
                statusText = "No Action"

            if statusText not in validStatuses:
                statusText = "Never Executed"

            pipelineName = element.inner_text()
            '''
            if pipelineName in pipelineStatusDict:  #SE HO GIA SALVATO LA PIPELINE NEL DICT, LA PAGINA NON E STATA RICARICATA, POICHE IL PULSANTE ERA DISATTIVATO
                exitLoop = True
                break
            '''
            print("Pipeline: " + str(pipelineName) + " *** Esito: " + str(statusText.strip()))  #DEBUGGING
            pipelineStatusDict[pipelineName] = statusText   #SALVO ALL'INTERNO DI UN DIZIONARIO, PER INSERIRLO SUCCESSIVAMENTE NEL FILE CSV DI OUTPUT

        page.click("text=Next")
        page.wait_for_timeout(2000) #ASPETTO IL CARICAMENTO DELLA NUOVA PAGINA

    saveDictAsCSV(pipelineStatusDict, "pipelineStatus.csv")

    #DEBUGGING
    page.screenshot()
    page.wait_for_timeout(4000)

    browser.close()