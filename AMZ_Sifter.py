from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import copy
import json

browser = webdriver.Firefox()
input("Please navigate to and pre-filter jobs. Press ENTER when ready.")
# Jobs URL is https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&category=software-development&job_type=Full-Time&cities[]=Irvine%2C%20California%2C%20USA&cities[]=Seattle%2C%20Washington%2C%20USA&cities[]=Portland%2C%20Oregon%2C%20USA&business_category[]=operations-technology&business_category[]=ecommerce-platform&business_category[]=amazon-devices&business_category[]=primevideo&business_category[]=amazongo&business_category[]=digital-entertainment&business_category[]=subsidiaries&business_category[]=amazon-books&category_type=Corporate&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=software&city=&country=&region=&county=&query_options=&

# Populate a list of jobs
jobs = []
while True:
    try:
        nextBtn = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, r'button[aria-label="Next page"]')))
        if nextBtn.get_attribute('aria-disabled') == 'true':
            break
    except:
        break
        # No more next buttons, we're done

    for job in WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, r'a.job-link'))):
        jobLink = job.get_attribute('href')
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
        if filter in str.lower(job[39:]):
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
        if filter in str(WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, r'div#sb-site div#job-detail div.content'))).get_attribute('innerHTML')).lower():
            try:
                doubleFilteredJobs.remove(job)
            except:
                continue

# Print out how many jobs we have left after source filtering
print(len(doubleFilteredJobs))
with open('amz_jobs.txt', 'w') as f:
    json.dump(doubleFilteredJobs, f)


