import slate3k as sl
import pandas as pd
name = "National Chart Data _ The COVID Tracking Project.pdf"
with open(name, "rb") as pdfObject:
    doc = sl.PDF(pdfObject)

    startIndex = 20
    endIndex = 0
    length = 34
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
#ds5 = pd.concat(ds5, row)
ds5.mask(ds5 == "", inplace=True)
ds5.dropna(axis=0, thresh=1, inplace=True)
ds5.drop([106], inplace=True)
ds5.rename(columns={0:"date",1:"new_cases"}, inplace=True)
ds5["date"] = pd.to_datetime(ds5["date"], '%d %b %Y').dt.strftime('="%m-%d-%Y"')

print(ds5)