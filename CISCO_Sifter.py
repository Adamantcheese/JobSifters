from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import copy
import json
import time

browser = webdriver.Firefox()
input("Please navigate to and pre-filter jobs. Press ENTER when ready.")
# Jobs URL is https://jobs.cisco.com/jobs/SearchJobs/?3_109_3=%5B%22169482%22%5D&3_143_3=%5B%2212229389%22%2C%2212229478%22%2C%2212229494%22%5D&3_19_3=%5B%22163%22%5D&3_12_3=%5B%22187%22%5D

# Populate a list of jobs
jobs = []
while True:
    # Cisco's website is really, REALLY slow to load, so we just wait a bunch of time
    time.sleep(5)
    try:
        nextBtn = None
        nextBtns = WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, r'a.pagination_item:not(.paginationLink)')))
        for button in nextBtns:
            if 'Next' in button.text:
                nextBtn = button
                break
        if nextBtn is None:
            raise Exception
    except:
        break
        # No more next buttons, we're done

    for job in WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, r'td[scope="row"]'))):
        jobLink = job.find_element_by_xpath(r'./a').get_attribute('href')
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
    lowerInitSub = str.lower(job[42:])
    upperSubInd = lowerInitSub.index('/')
    cut = lowerInitSub[:upperSubInd]
    for filter in urlFilters:
        if filter in cut:
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
    browser.get(job)
    for filter in sourceFilters:
        if filter in str(WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, r'div.section_content'))).get_attribute(
                'innerHTML')).lower():
            try:
                doubleFilteredJobs.remove(job)
            except:
                continue

# Print out how many jobs we have left after source filtering
print(len(doubleFilteredJobs))
with open('cisco_jobs.txt', 'w') as f:
    json.dump(doubleFilteredJobs, f)
