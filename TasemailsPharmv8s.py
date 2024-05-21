#!/usr/bin/env python3

from re import search
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")

# Specify the path to the ChromeDriver executable
chrome_driver_path = "/usr/local/bin/chromedriver"

# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


# Load the CSV file
csv_file = "securitiesmarketdata.csv"
df = pd.read_csv(csv_file)

# Verify column names
print("Column names in the CSV file:")
print(df.columns)

# Assuming the columns are 'R' for issuer number and 'A' for security number.
issuer_column = 'R'
security_column = 'A'

# Create a list to store company data
company_data = []

# Base URL structure
base_url = "https://market.tase.co.il/en/market_data/company/{issuer_number}/about?securityId={security_number}"

# Setup Selenium WebDriver
options = Options()
# options.headless = True  # Comment out headless mode for debugging
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--remote-debugging-port=9222")


# Function to extract email from a company page using CSS selector
def extract_email():
    try:
        email_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainContent > company-lobby > ng-component > company-details > section > div > company-info > div.company_page_box.row > div.col-lg-12.col-md-12.col-sm-12.col-xs-12.more_company_data.second-row > div > div:nth-child(3) > div.col-lg-12.col-md-12.col-sm-7.col-xs-7.company_data_value"))
        )
        email_text = email_element.text
        email = search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email_text)
        if email:
            return email.group(0)
        return None
    except Exception as e:
        print(f"Error extracting email: {e}")
        return None

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    issuer_number = row[issuer_column]
    security_number = row[security_column]
    url = base_url.format(issuer_number=issuer_number, security_number=security_number)
    
    try:
        driver.get(url)
        # Wait for the page to load
        time.sleep(10)
        
        email = extract_email()
        
        if email:
            company_data.append({"Issuer Number": issuer_number, "Email": email})
            print(f"Scraped email: {email}")
        else:
            print(f"No email found on page: {url}")

    except Exception as e:
        print(f"Error processing {url}: {e}")

# Close the driver
driver.quit()

# Save the data to an Excel file
df_output = pd.DataFrame(company_data)
df_output.to_excel("company_emails.xlsx", index=False)

print("Done scraping. Data saved to company_emails.xlsx")
