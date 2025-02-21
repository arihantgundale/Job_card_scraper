import time
from urllib.parse import quote
from selenium import webdriver
from job_scrapers import (
    linkedin_scraper,
    naukri_scraper
)
from selenium.webdriver.chrome.options import Options
from utils.file_utils import save_to_csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
import csv
import random


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


def main():
    job_title = input("Enter job title: ")
    location = input("Enter location: ")

    driver = configure_driver()
    all_jobs = []

    try:
         #scrape with random delays between platforms
        #all_jobs += linkedin_scraper.scrape_linkedin(driver, job_title, location)
        #time.sleep(random.randint(2, 5))

        #all_jobs += indeed_scraper.scrape_indeed(driver, job_title, location)
        #time.sleep(random.randint(2, 5))

       all_jobs += naukri_scraper.scrape_naukri(driver, job_title, location)
       time.sleep(random.randint(2, 5))


    except Exception as e:
        print(f"Main Error: {str(e)}")
    finally:
        driver.quit()

    if all_jobs:
        save_to_csv(all_jobs)
        print(f"Successfully saved {len(all_jobs)} jobs")
    else:
        print("No jobs found!")

if __name__ == "__main__":
    main()