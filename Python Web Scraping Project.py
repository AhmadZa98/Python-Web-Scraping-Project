from unittest import result
import requests
from itertools import zip_longest
import csv
from bs4 import BeautifulSoup

jobTitle = []
companyName = []
locationsName = []
Skills = []
links = []
salary = []
responsibilities = []
date = []
page_num = 0


while True:
    try:
        result = requests.get(
            "https://wuzzuf.net/search/jobs/?a=navbg%7Cspbg&q=django&start={page_num}")

        src = result.content

        soup = BeautifulSoup(src, "lxml")

        page_limit = int(soup.find("strong").text)

        if(page_limit > page_limit // 15):
            print("pages ended, terminate")
            break

        job_titles = soup.find_all("h2", {"class": "css-m604qf"})
        company_names = soup.find_all("a", {"class": "css-17s97q8"})
        locations_names = soup.find_all("span", {"class": "css-5wys0k"})
        job_skills = soup.find_all("div", {"class": "css-y4udm8"})
        posted_new = soup.find_all("span", {"class": "css-4c4ojb"})
        posted_old = soup.find_all("span", {"class": "css-do6t5g"})
        posted = [*posted_new, *posted_old]

        for i in range(len(job_titles)):
            jobTitle.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            companyName.append(company_names[i].text)
            locationsName.append(locations_names[i].text)
            Skills.append(job_skills[i].text)
            date_text = posted[i].text.replace("-", "").strip()
            date.append(date_text)

        page_num += 1
        print("page switched")
    except:
        print("error occurred")
        break

for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    salaries = soup.find("span", {"class": "css-4xky9y"})
    salary.append(salaries.text.strip())
    requirements = soup.find(
        "span", {"itemprop": "responsibilites"}).find("ul")
    respon_text = ""
    for li in requirements.find_all("li"):
        respon_text += li.text+"| "
    respon_text = respon_text[:-2]
    responsibilities.append(respon_text)

file_list = [jobTitle, companyName, date, locationsName,
             Skills, links, salary, responsibilities]
exported = zip_longest(*file_list)

with open("C:/Users/sakan/Desktop/Django FullStack/jobtutorial.csv", "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Job Title", "Company Name", "date", "Location",
                "Skills", "Links", "Salary", "responsibilities"])
    wr.writerows(exported)
