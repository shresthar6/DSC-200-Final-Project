import requests
from bs4 import BeautifulSoup
import pandas as pd

url= 'https://www.glassdoor.com/Job/data-science-jobs-SRCH_KO0,12.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data%2520science'
html = requests.get(url)

soup = BeautifulSoup(html.content, "html.parser")

job_title= []
company_name= []
city= []
state= []

for li in soup.find_all('li', class_='react-job-listing'):
    for div in li.find_all('div', class_='d-flex justify-content-between align-items-start'):
        company_name.append(div.text.strip())
    for a in li.find_all('a', class_='jobLink css-1rd3saf eigr9kq3'):
        for span in a.find_all('span'):
            job_title.append(span.text.strip())
    for div in li.find_all('div', class_='d-flex flex-wrap css-11d3uq0 e1rrn5ka2'):
        for span in div.find_all('span'):
            location= span.text.strip()
            # separates city and state
            if ',' in location:
                split = (location.split(", "))
                # adds city data
                city.append(split[0])
                # adds state data
                state.append(split[1])
            else:
                city.append(location)
                state.append(location)

df = pd.DataFrame({'job title': job_title, 'company name': company_name, 'city': city, 'state': state})
df.to_csv('Glassdoor.csv')