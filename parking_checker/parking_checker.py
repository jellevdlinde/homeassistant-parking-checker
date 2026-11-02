import asyncio
import json
import logging
from pathlib import Path
from playwright.async_api import async_playwright

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

URL = "https://app.myofficedays.com/"

async def main():
    logging.info("Parking Checker gestart")

    options_path = Path("/data/options.json")

    if options_path.exists():
        options = json.loads(options_path.read_text())
        username = options.get("username", "")
        password = options.get("password", "")
    else:
        username = ""
        password = ""

    if not username or not password:
        logging.error("Inloggegevens ontbreken.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context()
        page = await context.new_page()

        logging.info("My Office Days openen...")

        await page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        await page.wait_for_timeout(5000)

        logging.info("Paginatitel: %s", await page.title())
        logging.info("URL: %s", page.url)

        # Eerste test: bekijken welke pagina na het openen verschijnt.
        logging.info(
            "Pagina-inhoud: %s",
            (await page.locator("body").inner_text())[:3000]
        )

        logging.info("Eerste websitecontrole voltooid.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
