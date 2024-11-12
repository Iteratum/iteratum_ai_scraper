import asyncio
from playwright.async_api import async_playwright, Error
from bs4 import BeautifulSoup

async def init_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    return playwright, browser

async def scraped_content(browser, url):
    context = await browser.new_context()
    page = await context.new_page()

    try:
        print('Navigating to webpage...')
        await page.goto(url)
        print('Page loaded.')
        html_content = await page.content()
    except Error as e:
        print(f"Error occurred while loading page: {e}")
        html_content = None
    finally:
        await page.screenshot(path="page.png")
        await context.close()

    return html_content

async def main(url):
    playwright, browser = await init_browser()
    try:
        html_content = await scraped_content(browser, url)
        if html_content is None:
            raise ValueError("Failed to retrieve page content.")
    finally:
        await browser.close()
        await playwright.stop()
    return html_content

def extract_body_content(html_content):
    if not html_content:
        print("Warning: No HTML content provided.")
        return ""
        
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    if not body_content:
        print("Warning: No body content provided.")
        return ""
    
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

# To run the async main function from a synchronous script
if __name__ == "__main__":
    url = "https://example.com"  # Replace with the actual URL
    try:
        dom_content = asyncio.run(main(url))
        body_content = extract_body_content(dom_content)
        print(body_content)
    except Exception as e:
        print(f"Error in scraping process: {e}")
