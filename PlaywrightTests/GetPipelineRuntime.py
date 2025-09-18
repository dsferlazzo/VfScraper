from playwright.sync_api import sync_playwright
import argparse

parser = argparse.ArgumentParser(description='Last runtime scraper by given pipeline')
parser.add_argument("--filter", type=str, help="Name of the pipeline", default = "Import Product Hierarchy")   #PARAMETRO INSERIBILE ALL'INTERNO DELLA RIGA DI COMANDO
args = parser.parse_args()

with sync_playwright() as p:
    # Carica lo stato salvato
    browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe", headless=False)  # headless=False = mostra il browser
    context = browser.new_context(storage_state="state.json", device_scale_factor=1)
    page = context.new_page()
    page.set_viewport_size({"width": 1600, "height": 1200})

    page.goto("https://app.eu.visualfabriq.com/bifrost/nttdata/pipelines")

    page.get_by_placeholder("Search by name...").type(args.filter)
    page.wait_for_timeout(1000)
    page.locator(".bifrostcss-fFaJCf").nth(6).click()   #CLICCO SULLO STORICO DELLA PIPELINE
    page.wait_for_timeout(500)
    page.locator(".bifrostcss-bnFVuH").nth(0).click()   #CLICCO SULL'ULTIMA ESECUZIONE
    page.wait_for_timeout(500)
    print(page.locator(".bifrostcss-bItxDa").nth(0).inner_text())
    print(page.locator(".bifrostcss-bItxDa").nth(1).inner_text())