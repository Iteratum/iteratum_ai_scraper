from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import random
import time

# Initialize the Playwright browser
def init_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)  # Set headless=True if you don't need a UI
    context = browser.new_context(
        user_agent=random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        ])
    )
    return playwright, browser, context

# Mimic human-like scrolling and random delays
def mimic_human_behavior(page):
    last_height = page.evaluate("document.body.scrollHeight")
    while True:
        scroll_distance = random.randint(300, 800)
        page.evaluate(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(1, 3))  # Random delay to mimic human reading
        
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scraped_content(context, url):
    page = context.new_page()
    print('Navigating to webpage...')
    page.goto(url)
    print('Page loaded. Mimicking human behavior...')
    
    # Mimic human-like behavior
    mimic_human_behavior(page)
    
    print('Capturing screenshot for debugging...')
    page.screenshot(path="page.png")
    
    # Extract HTML content
    html = page.content()
    print("HTML content captured")
    return html

def main(url):
    playwright, browser, context = init_browser()
    try:
        html_content = scraped_content(context, url)
    finally:
        browser.close()
        playwright.stop()
    return html_content

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]