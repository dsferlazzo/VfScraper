from playwright.sync_api import sync_playwright
import argparse

parser = argparse.ArgumentParser(description='Visualfabriq login status saver')
parser.add_argument("--organisationId", type=str, help="Organization id", default = "")   #PARAMETRO INSERIBILE ALL'INTERNO DELLA RIGA DI COMANDO
parser.add_argument("--mail", type=str, help="Account mail", default = "")   #PARAMETRO INSERIBILE ALL'INTERNO DELLA RIGA DI COMANDO
parser.add_argument("--password", type=str, help="Account password", default = "")   #PARAMETRO INSERIBILE ALL'INTERNO DELLA RIGA DI COMANDO
args = parser.parse_args()


#SCRIPT PER SALVARE LO STATO DEL LOGIN IN 'state.json', IN MODO DA POTER ESSERE UTILIZZATO NEGLI ALTRI SCRIPT
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",headless=False)  # headless=False = mostra il browser

    page = browser.new_page()
    page.goto("https://app.eu.visualfabriq.com/dashboard")

    #EFFETTU0 IL LOGIN SECONDO I PARAMETRI PASSATI NELLA RIGA DI COMANDO
    page.type("#login-sso-organisation-id", args.organisationId)    #INSERISCO L'ORGANIZATION ID
    page.wait_for_timeout(500)
    page.click("text=Continue")
    page.type("#i0116", args.mail)  #INSERISCO LA MAIL
    page.wait_for_timeout(500)
    page.click("text=Avanti")
    page.type("#passwordInput", args.password)  #INSERISCO LA PASSWORD
    page.wait_for_timeout(500)
    page.click("#submitButton")
    page.click("#idSIButton9")
    page.wait_for_timeout(8000) #ASPETTO CHE LA PAGINA VENGA CARICATA COMPLETAMENTE

    # Salva lo stato di login (cookie + localStorage) in un file
    page.context.storage_state(path="state.json")
    print("Login file 'state.json' created correctly")
    browser.close()
