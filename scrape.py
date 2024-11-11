from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os

def init_driver():
    # Set up BrowserStack options
    browserstack_options = {
        "os": "Windows",
        "os_version": "10",
        "browser": "Chrome",
        "browser_version": "latest",
        "name": "Streamlit App Test",
        "build": "Streamlit App Build"
    }
    
    options = webdriver.ChromeOptions()
    options.set_capability("bstack:options", browserstack_options)
    
    # Set BrowserStack credentials
    username = os.getenv("BROWSERSTACK_USERNAME")
    access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    browserstack_url = f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub"

    return webdriver.Remote(
        command_executor=browserstack_url,
        options=options
    )

def scraped_content(driver, url):
    driver.get(url)
    html = driver.page_source
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
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
