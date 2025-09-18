from playwright.sync_api import sync_playwright
from datetime import datetime

def scrape_pipeline_last_run(pipeline_filter: str) -> dict:
    """
    Scrapes the last pipeline execution filtered by name.
    Returns a dictionary with start time, finish time, and duration in minutes.
    """
    with sync_playwright() as p:
        # Launch browser (using Chrome already installed)
        browser = p.chromium.launch(
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            headless=True  # Does not open a window
        )
        context = browser.new_context(storage_state="state.json", device_scale_factor=1)
        page = context.new_page()
        page.set_viewport_size({"width": 1600, "height": 1200})

        # Go to the page
        page.goto("https://app.eu.visualfabriq.com/bifrost/nttdata/pipelines")

        # Filter pipeline
        page.get_by_placeholder("Search by name...").type(pipeline_filter)
        page.wait_for_timeout(1000)

        # Click pipeline elements
        page.locator(".bifrostcss-fFaJCf").nth(6).click()   # history
        page.wait_for_timeout(500)
        page.locator(".bifrostcss-bnFVuH").nth(0).click()   # last execution
        page.wait_for_timeout(500)

        # Extract start and finish times (as strings from the page)
        startTime = page.locator(".bifrostcss-bItxDa").nth(0).inner_text()
        finishTime = page.locator(".bifrostcss-bItxDa").nth(1).inner_text()

        # Cleanup browser
        context.close()
        browser.close()

        # Try to compute duration in minutes
        duration_minutes = None
        try:
            dt_format = "%d/%m/%Y, %H:%M:%S %Z"
            start_dt = datetime.strptime(startTime, dt_format)
            finish_dt = datetime.strptime(finishTime, dt_format)
            duration_minutes = (finish_dt - start_dt).total_seconds() / 60.0
        except Exception as e:
            # If parsing fails, keep duration as None
            duration_minutes = None

        return {
            "pipeline_name": pipeline_filter,
            "start_time": startTime,
            "finish_time": finishTime,
            "duration_minutes": duration_minutes
        }
