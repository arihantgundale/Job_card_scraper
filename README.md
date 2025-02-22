# Job_card_scraper

WEB SCRAPPER

This project automates the extraction of job listings from LinkedIn and Naukri using Selenium. The scraped data (title, company, location, link, etc.) is saved to a CSV file. The code is modular, with separate components for scraping, driver configuration, and file handling.

Project Structure:  

Required dependencies:
Package	Purpose
Selenium	Browser automation
csv	CSV file operations
urllib.parse	URL encoding
time	Delay management

Installation:
Using pip install
Eg.   pip install selenium





Key components:
1. Driver Configuration (configure_driver())
•	Uses headless Chrome with anti-bot detection flags.
•	Chromedriver Path: Update in all configure_driver() functions if needed.
•	Example configuration: 

options.add_argument("--disable-blink-features=AutomationControlled")
service = Service("/path_to_chromedriver")

2. LinkedIn Scraper (linkedin_scraper.py)

•	Authentication: Uses hardcoded credentials (security risk in production).
•	URL Format: https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}
•	Data Collected:
{
  "Title": "  ",
  "Company": " ",
  "Location": " ",
  "Type": "  ",
  "Link": "https://linkedin.com/jobs/123",
  "Platform": "LinkedIn"
}

3. Naukri Scraper (naukri_scraper.py)
•	URL Format: https://www.naukri.com/{job_title}-jobs-in-{location}
•	Scrolls to load additional jobs.
•	Same data as above is collected

4. CSV Saving (file_utils.py)
•	Output Path: as described by the user
•	Fields: title, company, location, link, timestamp
•	Appends data to existing files.



Setup Instructions
1.	Install Chromedriver:
o	Download from Chromedriver
o	Update path in all configure_driver() functions:
service = Service("/your_chromedriver_path")
2.	Run the Script:
python main.py

3.	Enter job title and location when prompted.

4.	Open the csv file at given location to find the information about the job card




 

 
 

 
 














 
