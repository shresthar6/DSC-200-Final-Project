import requests
from bs4 import BeautifulSoup
import pandas as pd
from csv import writer
import numpy as np
import slate3k as sl

def part1():
    print("Part 1")
    ds1 = part1_DS1()
    ds2 = part1_DS2()
    part1_DS3()
    ds3 = pd.read_csv("ds3.csv")
    ds4 = part1_DS4()
    ds5 = part1_DS5()

    ds3["date"] = pd.to_datetime(ds3["date"]).dt.strftime('="%m-%d-%Y"')
    #ds5["date"] = pd.to_datetime(ds5["date"], '%d %b %Y').dt.strftime('="%m-%d-%Y"')

    df = pd.merge(ds1, ds2, how="outer", on="date")
    df = pd.merge(df, ds3, how="outer", left_on=["date", "area"], right_on=["date", "state"])
    df = pd.merge(df, ds4, how="outer", on="date")
    df = pd.merge(df, ds5, how="outer", left_on="date", right_on="date")
    df.drop_duplicates(inplace=True)
    df.mask(df == "", inplace=True)
    df.dropna(axis=0, thresh=5, inplace=True)
    df.to_csv("group_6_covid.csv", index=False)
    
def part1_DS1() -> pd.DataFrame:
    # varient data
    ds1 = pd.read_csv("https://data.chhs.ca.gov/dataset/52e4aa7a-2ea3-4bfd-8cd6-7d653db1ee74/resource/d7f9acfa-b113-4cbc-9abc-91e707efc08a/download/covid19_variants.csv")
    #ds1.to_csv('ds1.csv')
    return ds1

# csv
def part1_DS2() -> pd.DataFrame:
    # vaccine progress dashboard
    ds2 = pd.read_csv("https://data.chhs.ca.gov/dataset/e283ee5a-cf18-4f20-a92c-ee94a2866ccd/resource/22b05bf3-16e5-4b2b-a66a-6b035e0cd9f4/download/covid19vaccinesadministeredbyhpiquartile.csv")
    ds2.rename(columns={"administered_date":"date"}, inplace=True)
    #ds2.to_csv('ds2.csv')
    return ds2

# api
def part1_DS3():
    url = "https://api.covidtracking.com/v1/states/ca/daily.json"
    response = requests.request("GET", url, headers=None, data=[])

    json_file = response.json()
    #print(json_file)

    column = []
    header = ["date", "state", "positive", "deaths", "deathIncrease", "negativeIncrease", "positiveIncrease", "positiveCasesViral"]

    for i in json_file:
        # you can edit what data we need to merge with other files
        row = (i["date"], i["state"], i["positive"], i["death"], i["deathIncrease"], i["negativeIncrease"], i["positiveIncrease"], i["positiveCasesViral"])
        column.append(row)

    # writing a csv file
    with open("ds3.csv", "w") as wFileObj:
        m_writer = writer(wFileObj)
        m_writer.writerow(header)
        m_writer.writerows(column)

# excel
def part1_DS4() -> pd.DataFrame:
    ds4 = pd.read_excel("https://github.com/thohan88/covid19-nor-data/raw/master/data/04_deaths/deaths_total_fhi.xlsx")
    #ds4.to_csv("ds4.csv", index=False)
    return ds4

# pdf
def part1_DS5() -> pd.DataFrame:
    name = "National Chart Data _ The COVID Tracking Project.pdf"
    with open(name, "rb") as pdfObject:
        doc = sl.PDF(pdfObject)

        date = []
        new_cases = []
        row = []
        count = 0

        for index, page in enumerate(doc):
            #print(page.split("\n"))
            data = page.split("\n")
            if(index == 0):
                dateLow = 21
                dateHigh = 54
                casesLow = 65
                casesHigh = 132
            elif(index == 1):
                dateLow = 216
                dateHigh = 253
                casesLow = 263
                casesHigh = 320
            elif(index == 2):
                dateLow = 423
                dateHigh = 460
                casesLow = 470
                casesHigh = 507
            elif(index >= 3):
                dateLow += 103
                dateHigh += 37
                casesLow += 10
                casesHigh += 37
        

            for element in data:
                count += 1
                if(count >= dateLow and count < dateHigh):
                    date.append(element)
                if(count >= casesLow and count < casesHigh):
                    new_cases.append(element)
        
        for i in range(len(date)):
            row.append([date[i], new_cases[i]])

    ds5 = pd.DataFrame(row)
    ds5.mask(ds5 == "", inplace=True)
    ds5.dropna(axis=0, thresh=1, inplace=True)
    ds5.drop([106], inplace=True)
    ds5.rename(columns={0:"date",1:"new_cases"}, inplace=True)

    return ds5

def part2():
    print("Part 2")
    ds1 = part2_DS1()
    ds2 = part2_DS2()

    ds1["qualifications"] = ds1["qualifications"].apply(tuple)
    ds2["qualifications"] = ds2["qualifications"].apply(tuple)
    df = pd.merge(ds1, ds2, how="outer", on=["job title", "company name", "salary", "city", "state", "qualifications"])
    df = pd.merge(df, part2_DS3(), how='outer', on=["job title", "company name", "city", "state", "qualifications"])
    df = df[df["job title"].str.contains("Data|DATA|data") == True]
    #df.drop_duplicates(inplace=True)
    df.to_csv("group_6_dsc_jobs.csv", index=False)

def part2_DS1() -> pd.DataFrame:
    url= 'https://www.simplyhired.com/search?q=data+science&l=&job=f6OiCClL7m7gOAQ9o5ElmNquyKreuYz_0b-j3kwtgZ4_mb69UV9KQQ'
    html = requests.get(url)

    soup = BeautifulSoup(html.content, "html.parser")

    salary=[]
    job_title=[]
    company_name=[]
    city=[]
    state=[]
    job_type=[]
    qualifications=[]
    type= []
    
    # adds job title to list
    for a in soup.find_all('a', class_='SerpJob-link card-link'):
        job_title.append(a.text.strip())
    # adds salary to list
    for div in soup.find_all('div', class_=['SerpJob-metaInfoLeft']):
        if div.text == '':
            salary.append('N/A')
        else:
            salary.append(div.text.strip('Estimated: ').strip('Quick Apply').strip('a year'))
    # adds compant name to list
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
            state.append('N/A')
            
    # link for all job detail pages are added to links list
    links=[]
    for a in soup.find_all('a', class_='SerpJob-link card-link'):
        link= 'https://www.simplyhired.com' + a["href"]
        links.append(link)

    for link in links:
        html2= requests.get(link)
        soup2= BeautifulSoup(html2.content, 'html.parser')
        for div in soup2.find_all('div', class_='viewjob-content'):
            for div in div.find_all('div', class_='viewjob-section viewjob-qualifications viewjob-entities'):
                # qualifications added to list
                for ul in div.find_all('ul', class_='Chips'):
                    a= []
                    for li in ul.find_all('li', class_='viewjob-qualification'):
                        a.append(li.text.strip())
            
                    qualifications.append(a)
        # adds job type to list if available
        try:
            for div in soup2.find_all('div', class_='viewjob-section'):
                for span in div.find_all('span', class_='viewjob-labelWithIcon viewjob-jobType'):
                    type.append(span.text.strip())
        except:
            type.append(' ')

    a = ({'job title': job_title, 'company name': company_name, 'salary': salary, 'city': city, 'state': state, 'job type': type, 'qualifications': qualifications})
    df= pd.DataFrame.from_dict(a, orient='index')
    df = df.transpose()
    df.to_csv("1.csv")
    return df

def part2_DS2() -> pd.DataFrame:
    url= 'https://www.glassdoor.com/Job/data-science-jobs-SRCH_KO0,12.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data%2520science'
    html = requests.get(url)

    soup = BeautifulSoup(html.content, "html.parser")

    job_title= []
    company_name= []
    city= []
    state= []
    salary= []

    for li in soup.find_all('li', class_='react-job-listing'):
        # adds company name to list
        for div in li.find_all('div', class_='d-flex justify-content-between align-items-start'):
            company_name.append(div.text.strip())
        # adds job title to list
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
    # adds salary to list
    for div in soup.find_all('div', class_=['css-19txzrf e14vl8nk0x', 'css-3g3psg pr-xxsm']):
        if '$' in div.text:
            for span in div.find_all('span', class_='css-1xe2xww e1wijj242'):
                salary.append(span.text.strip())
        else:
            salary.append(' ')
    # link for all job detail pages are added to links list
    links=[]
    for a in soup.find_all('a', class_='jobLink css-1rd3saf eigr9kq3'):
        link= 'https://www.glassdoor.com' + a["href"]
        links.append(link)

    a = ({'job title': job_title, 'company name': company_name, 'salary': salary, 'city': city, 'state': state, 'qualifications': links})
    df= pd.DataFrame.from_dict(a, orient='index')
    df = df.transpose()
    df.to_csv("2.csv")
    return df
              
def part2_DS3() -> pd.DataFrame:
    url= 'https://jooble.org/SearchResult?ukw=data%20science'
    html = requests.get(url)

    soup = BeautifulSoup(html.content, "html.parser")

    job_title= []
    company_name= []
    city= []
    state= []
    qualifications= []
    
    # adds job title to list
    for h2 in soup.find_all('h2', class_='_15V35X'):
        job_title.append(h2.text.strip())
    # adds company name to list
    for div in soup.find_all('div', class_='_3lDiEO'):
        company_name.append(div.text.strip())
    for div in soup.find_all('div', class_='caption _2_Ab4T'):
        location= div.text.strip()
        # separates city and state
        if ',' in location:
            split = (location.split(", "))
            # adds city data to list
            city.append(split[0])
            # adds state data to list
            state.append(split[1])
        else:
            city.append(location)
            state.append('N/A')

    links=[]
    # link for all job detail pages are added to links list
    for h2 in soup.find_all('h2', class_='_15V35X'):
        for a in h2.find_all('a'):
            link= a["href"]
            links.append(link)

    a = ({'job title': job_title, 'company name': company_name, 'city': city, 'state': state, 'qualifications': links})
    df= pd.DataFrame.from_dict(a, orient='index')
    df = df.transpose()
    df.to_csv("3.csv")
    return df

print("Welcome to the final project!")

state = True

while(state):

    choice = int(input("Please enter which part you wish to run (1)Covid (2)DSC Jobs (3)Quit: "))
    while(choice < 1 or choice > 3):
        choice = int(input("%d is not a valid choice. Please try again: "%choice))

    if(choice == 1):
        part1()
    elif(choice == 2):
        part2()
    else:
        state = False
