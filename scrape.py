from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random

# Initialize the Selenium WebDriver
def init_driver():
    # Path to your ChromeDriver; specify if necessary
    chrome_service = Service(executable_path='chromedriver.exe')
    options = ChromeOptions()
    
    # Add realistic user-agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    # Enable headless mode if desired
    # options.add_argument("--headless")
    
    # Disable detection of automated browsing
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    # Initialize WebDriver
    return webdriver.Chrome(service=chrome_service, options=options)

# Mimic human-like scrolling and random delays
def mimic_human_behavior(driver):
    # Scroll to the bottom of the page slowly
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down a random portion of the page
        scroll_distance = random.randint(300, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(1, 3))  # Random delay to mimic human reading
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scraped_content(driver, url):
    print('Navigating to webpage...')
    driver.get(url)
    print('Page loaded. Mimicking human behavior...')
    
    # Mimic human-like behavior
    mimic_human_behavior(driver)
    
    print('Capturing screenshot for debugging...')
    driver.save_screenshot("page.png")
    
    # Extract HTML content
    html = driver.page_source
    print("HTML content captured")
    return html

def main(url):
    driver = init_driver()
    try:
        html_content = scraped_content(driver, url)
    finally:
        driver.quit()
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
