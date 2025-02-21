import time
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass


def configure_driver():
    """
    Configures and returns a Selenium WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Use Service() to specify the ChromeDriver path
    service = Service("/opt/homebrew/bin/chromedriver")  # Update this path if necessary

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver


from selenium.webdriver.common.keys import Keys


def login(driver, username="arhxpvt@gmail.com", password="Admin@123"):
    driver.get("https://www.linkedin.com/login")

    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = driver.find_element(By.ID, "password")

        email_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Wait for login to complete
        WebDriverWait(driver, 10).until(
            lambda d: "feed" in d.current_url or "mynetwork" in d.current_url
        )

        print("Successfully logged in.")

    except Exception as e:
        print(f"Login failed: {e}")
        driver.save_screenshot("login_error.png")
        raise


def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(3):  # Scroll multiple times to load more jobs
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scrape_linkedin(driver, job_title, location):
    print("Scraping LinkedIn...")
    jobs = []
    try:
        url = f"https://www.linkedin.com/jobs/search/?keywords={quote(job_title)}&location={quote(location)}"
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".base-card:not(.ad-banner)"))
        )
        scroll_page(driver)

        job_cards = driver.find_elements(By.CSS_SELECTOR, ".base-card:not(.ad-banner)")
        for card in job_cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, "h3.base-search-card__title").text.strip()
                company = card.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle").text.strip()
                location = card.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text.strip()
                link = card.find_element(By.CSS_SELECTOR, "a.base-card__full-link").get_attribute("href")
                job_type = card.find_element(By.CSS_SELECTOR,
                                             "span.job-search-card__workplace-type").text.strip() if card.find_elements(
                    By.CSS_SELECTOR, "span.job-search-card__workplace-type") else "Not specified"

                jobs.append({"Title": title, "Company": company, "Location": location, "Type": job_type, "Link": link,
                             "Platform": "LinkedIn"})
            except NoSuchElementException:
                continue
    except TimeoutException:
        print("LinkedIn: Timeout while loading jobs")

    return jobs
