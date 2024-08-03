from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.linkedin.com/in/mandyfransz/")
time.sleep(2)

source = driver.page_source
soup = BeautifulSoup(source, 'html.parser')

with open("linkedin.txt", "w", errors = "ignore") as f:
    f.write(source)
# Extract the structured JSON data
script_tag = soup.find('script', {'type': 'application/ld+json'})
structured_data = json.loads(script_tag.string)

# Extract the first name, last name, companies, and job titles
name = structured_data["@graph"][0]["name"]
works_for = structured_data["@graph"][0]["worksFor"]
job_titles = structured_data["@graph"][0]["jobTitle"]

# Print the name
print(f"Name: {name}")

# Print the companies and job titles
for company, title in zip(works_for, job_titles):
    company_name = company["name"]
    print(f"Company: {company_name}, Title: {title}")
time.sleep(50)
driver.quit()
