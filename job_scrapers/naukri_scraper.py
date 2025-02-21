import time
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service


def configure_driver():
    """Configures and returns a Selenium WebDriver instance."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

        service = Service("/opt/homebrew/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(60)
        driver.implicitly_wait(10)
        return driver
    except Exception as e:
        print(f"Error configuring driver: {str(e)}")
        return None


def scroll_page(driver):
    """Scrolls down the page gradually to load more job postings."""
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    except Exception as e:
        print(f"Scroll error: {str(e)}")


def scrape_naukri(driver, job_title, location):
    print("Scraping Naukri...")
    jobs = []

    if not driver:
        print("Failed to initialize driver")
        return jobs

    try:
        url = f"https://www.naukri.com/{quote(job_title.lower().replace(' ', '-'))}-jobs-in-{quote(location.lower().replace(' ', '-'))}"
        print(f"Loading URL: {url}")
        driver.get(url)

        time.sleep(5)

        # Wait for job listings container
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
            )
            print("Job listings wrapper found")
        except TimeoutException:
            print("Page structure debug:", driver.page_source[:500])
            raise TimeoutException("Main job wrapper not found")

        scroll_page(driver)

        # Updated selector for job cards - using more current class name
        job_cards = driver.find_elements(By.CLASS_NAME, "cust-job-tuple")
        print(f"Found {len(job_cards)} job cards")

        if len(job_cards) == 0:
            # Debug: Try alternative selector and print some page content
            job_cards_alt = driver.find_elements(By.CSS_SELECTOR, "div.cust-job-tuple")
            print(f"Alternative selector found {len(job_cards_alt)} job cards")
            print("Sample page content:", driver.page_source[500:1000])

        for card in job_cards:
            try:
                # Updated selectors based on current Naukri structure
                title_elem = card.find_elements(By.CLASS_NAME, "title")
                title = title_elem[0].text.strip() if title_elem else "N/A"

                company_elem = card.find_elements(By.CLASS_NAME, "company")
                company = company_elem[0].text.strip() if company_elem else "N/A"

                location_elem = card.find_elements(By.CLASS_NAME, "locWdth")
                location = location_elem[0].text.strip() if location_elem else "N/A"

                exp_elem = card.find_elements(By.CLASS_NAME, "expwdth")
                experience = exp_elem[0].text.strip() if exp_elem else "N/A"

                link_elem = card.find_elements(By.CLASS_NAME, "title")
                link = link_elem[0].get_attribute("href") if link_elem else "N/A"

                jobs.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Experience": experience,
                    "Link": link,
                    "Platform": "Naukri"
                })
            except Exception as e:
                print(f"Error processing job card: {str(e)}")
                continue

        print(f"Successfully scraped {len(jobs)} jobs")

    except TimeoutException as e:
        print(f"Timeout error: {str(e)}")
    except WebDriverException as e:
        print(f"WebDriver error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        driver.quit()

    return jobs