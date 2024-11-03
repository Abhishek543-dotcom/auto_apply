import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open LinkedIn job listings URL
driver.get(
    "https://www.linkedin.com/jobs/search/?keywords=Data%20Engineer&location=India&geoId=102713980&f_TPR=r86400&position=1&pageNum=0")

# Scroll to the bottom to load all job postings
SCROLL_PAUSE_TIME = 2

# Make sure the body element is present before executing the script
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
except TimeoutException:
    print("Timed out waiting for the page to load the body element.")
    driver.quit()
    exit()

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Debugging: Print the page source to verify content
print(driver.page_source[:1000])  # Print first 1000 characters for inspection

# Wait for job listings to be present
try:
    jobs = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.jobs-search__results-list li'))
    )
    print(f"Found {len(jobs)} job listings.")
except TimeoutException:
    print("Timed out waiting for the job listings to load.")
    driver.quit()
    exit()

# Extract job details
job_data = []
job_links = []

# First, collect all job links
for job in jobs:
    try:
        job_link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        job_links.append(job_link)
    except NoSuchElementException:
        print("Error finding job link element.")
    except Exception as e:
        print(f"Error collecting job link: {e}")

# Now, visit each job link to collect details
for index, job_link in enumerate(job_links):
    driver.get(job_link)
    time.sleep(3)  # Give the page time to load

    try:
        # Extract job details
        try:
            title = driver.find_element(By.CSS_SELECTOR, 'h1.topcard__title').text.strip()
        except NoSuchElementException:
            title = "Title not found"

        try:
            company = driver.find_element(By.CSS_SELECTOR, 'a.topcard__org-name-link').text.strip()
        except NoSuchElementException:
            company = "Company not found"

        try:
            location = driver.find_element(By.CSS_SELECTOR, 'span.topcard__flavor--bullet').text.strip()
        except NoSuchElementException:
            location = "Location not found"

        try:
            date_posted = driver.find_element(By.CSS_SELECTOR, 'span.topcard__flavor--metadata').text.strip()
        except NoSuchElementException:
            date_posted = "Date posted not found"

        # Click "See more" if available to get full job description
        try:
            see_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.show-more-less-html__button'))
            )
            see_more_button.click()
        except TimeoutException:
            print(f"No 'See more' button found for job {index + 1}.")

        # Get the job description
        try:
            job_description = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.show-more-less-html__markup'))
            ).text.strip()
        except TimeoutException:
            job_description = "Job description not found"

        # Append the job details to the list
        job_data.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Date Posted": date_posted,
            "Job Link": job_link,
            "Job Description": job_description
        })

    except Exception as e:
        print(f"Error processing job {index + 1}: {e}")

# Save the data into a CSV file
df = pd.DataFrame(job_data)
df.to_csv('linkedin_jobs_with_full_descriptions.csv', index=False)

# Close the browser
driver.quit()

print("Data has been saved to linkedin_jobs_with_full_descriptions.csv")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open LinkedIn job listings URL
driver.get("https://www.linkedin.com/jobs/search/?keywords=Data%20Engineer&location=India&geoId=102713980&f_TPR=r86400&position=1&pageNum=0")

# Scroll to the bottom to load all job postings
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Debugging: Print the page source to verify content
print(driver.page_source[:1000])  # Print first 1000 characters for inspection

# Wait for job listings to be present
try:
    jobs = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.jobs-search__results-list li'))
    )
    print(f"Found {len(jobs)} job listings.")
except TimeoutException:
    print("Timed out waiting for the job listings to load.")
    driver.quit()
    exit()

# Extract job details
job_data = []
job_links = []

# First, collect all job links
for job in jobs:
    try:
        job_link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        job_links.append(job_link)
    except NoSuchElementException:
        print("Error finding job link element.")
    except Exception as e:
        print(f"Error collecting job link: {e}")

# Now, visit each job link to collect details
for index, job_link in enumerate(job_links):
    driver.get(job_link)
    time.sleep(3)  # Give the page time to load

    try:
        # Extract job details
        try:
            title = driver.find_element(By.CSS_SELECTOR, 'h1.topcard__title').text.strip()
        except NoSuchElementException:
            title = "Title not found"

        try:
            company = driver.find_element(By.CSS_SELECTOR, 'a.topcard__org-name-link').text.strip()
        except NoSuchElementException:
            company = "Company not found"

        try:
            location = driver.find_element(By.CSS_SELECTOR, 'span.topcard__flavor--bullet').text.strip()
        except NoSuchElementException:
            location = "Location not found"

        try:
            date_posted = driver.find_element(By.CSS_SELECTOR, 'span.topcard__flavor--metadata').text.strip()
        except NoSuchElementException:
            date_posted = "Date posted not found"

        # Click "See more" if available to get full job description
        try:
            see_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.show-more-less-html__button'))
            )
            see_more_button.click()
        except TimeoutException:
            print(f"No 'See more' button found for job {index + 1}.")

        # Get the job description
        try:
            job_description = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.show-more-less-html__markup'))
            ).text.strip()
        except TimeoutException:
            job_description = "Job description not found"

        # Append the job details to the list
        job_data.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Date Posted": date_posted,
            "Job Link": job_link,
            "Job Description": job_description
        })

    except Exception as e:
        print(f"Error processing job {index + 1}: {e}")

# Save the data into a CSV file
df = pd.DataFrame(job_data)
df.to_csv('data_files/linkedin_jobs_details.csv', index=False)

# Close the browser
driver.quit()

print("Data has been saved to linkedin_jobs_with_full_descriptions.csv")
