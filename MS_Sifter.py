import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import copy

browser = webdriver.Firefox()
input("Please navigate to and pre-filter jobs. Press ENTER when ready.")
# Jobs URL is https://careers.microsoft.com/us/en/search-results?rt=professional&keywords=software

# Populate a list of jobs
jobs = []
while True:
    try:
        nextBtn = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, r'a[aria-label="View Next page"]')))
    except:
        break
        # No more next buttons, we're done

    for job in WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, r'span.job-title'))):
        jobListing = job.find_element_by_xpath('..')
        jobLink = jobListing.get_attribute('href')
        jobs.append(jobLink)

    nextBtn.click()

# Populate a list of URL filters
urlFilters = []
with open('url_filter.txt') as filterFile:
    for filter in filterFile.readlines():
        urlFilters.append(filter.strip())

# Copy the job list and filter it
filteredJobs = copy.deepcopy(jobs)
for job in jobs:
    for filter in urlFilters:
        if filter in str.lower(job[47:]):
            try:
                filteredJobs.remove(job)
            except:
                continue

# Populate a list of page source filters
sourceFilters = []
with open('source_filter.txt') as sourceFilterFile:
    for filter in sourceFilterFile.readlines():
        sourceFilters.append(filter.strip())

# Print out how many jobs we have left after URL filtering
print(len(filteredJobs))

# Filter jobs with page source filters
doubleFilteredJobs = copy.deepcopy(filteredJobs)
for job in filteredJobs:
    try:
        browser.get(job)
        innerHTML = str(WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, r'section.job-description'))).get_attribute('innerHTML')).lower()
        for filter in sourceFilters:
            if filter in innerHTML:
                try:
                    doubleFilteredJobs.remove(job)
                except:
                    continue
    except:
        continue

# Print out how many jobs we have left after source filtering
print(len(doubleFilteredJobs))
with open('ms_jobs.txt', 'w') as f:
    json.dump(doubleFilteredJobs, f)

browser.quit()


