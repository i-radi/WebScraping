# pip install lxml
# pip install requests
# pip install bs4

import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title = []
company_name = []
location_name = []
skills = []
links = []
salary = []
responsibilities = []
date = []
page_num = 0
Url = "https://wuzzuf.net/search/jobs/?a=spbg&q=python&start="

while True:
    try:
        result = requests.get(Url + str(page_num))

        src = result.content

        soup = BeautifulSoup(src, "lxml")

        page_limit = int(soup.find("strong").text)

        if (page_num > page_limit // 15):
            print("Pages ended, terminate")
            break

        job_titles = soup.find_all("h2", {"class": "css-m604qf"})
        company_names = soup.find_all("a", {"class": "css-17s97q8"})
        location_names = soup.find_all("span", {"class": "css-5wys0k"})
        job_skills = soup.find_all("div", {"class": "css-y4udm8"})
        # posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
        # posted_old = soup.find_all("div", {"class": "css-do6t5g"})
        # posted = [*posted_new, *posted_old]
        jobTempletes = soup.find_all( "div", {"class":"css-1o5ybe7 e1581u7e0"})


        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            location_name.append(location_names[i].text)
            skills.append(job_skills[i].text)
            if jobTempletes[i].find("div", {"class":"css-do6t5g"}):
                date_job = jobTempletes[i].find("div", {"class":"css-do6t5g"})
            elif jobTempletes[i].find("div", {"class":"css-4c4ojb"}):
                date_job =  jobTempletes[i].find("div", {"class":"css-4c4ojb"})
            date.append(date_job.text.replace("-","").strip())

        page_num += 1
        print(f"page switched {page_num}")
    except:
        print("error occurred")
        break

job_num = 0
for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    salaries = soup.find("div", {"class": "matching-requirement-icon-container", "data-toggle": "tooltip",
                                 "data-placement": "top"})
    salary.append(salaries.text.strip())
    requirments = soup.find("span", {"itemprop": "responsibilities"}).ul
    respon_text = ""
    for li in requirments.find_all("li"):
        respon_text += li.text + "|"
    respon_text = respon_text[:-2]
    responsibilities.append(respon_text)
    job_num += 1
    print(f"Job {job_num} done")

file_list = [job_title, company_name, date, location_name, skills, links, salary, responsibilities]
exported = zip_longest(*file_list)

with open('D:\jobs.csv', "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["job title", "company name", "date", "location", "skills", "links", "salary", "responsibilities"])
    wr.writerows(exported)
print("Done")
