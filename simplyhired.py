import requests
from bs4 import BeautifulSoup
import pandas as pd

url= 'https://www.simplyhired.com/search?q=data+science&l=&job=f6OiCClL7m7gOAQ9o5ElmNquyKreuYz_0b-j3kwtgZ4_mb69UV9KQQ'
html = requests.get(url)

soup = BeautifulSoup(html.content, "html.parser")

salary=[]
job_title=[]
company_name=[]
city=[]
state=[]
job_type=[]

for a in soup.find_all('a', class_='SerpJob-link card-link'):
    job_title.append(a.text.strip())

for div in soup.find_all('div', class_=['SerpJob-metaInfoLeft']):
    if div.text == '':
        salary.append('Unknown')
    else:
        salary.append(div.text.strip('Estimated: ').strip('Quick Apply').strip('a year'))

for span in soup.find_all('span', class_='JobPosting-labelWithIcon jobposting-company'):
    company_name.append(span.text.strip())

for span in soup.find_all('span', class_='JobPosting-labelWithIcon jobposting-location'):
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

df = pd.DataFrame({'job title': job_title, 'company name': company_name, 'salary': salary, 'city': city, 'state': state})
df.to_csv('simplyhired.csv')