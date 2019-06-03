#this is for extracting HARRIS-County-Data from https://www.zip-codes.com/.
                                                        #yang cao, 6/1/2019.
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

start_time = time.time()
url = 'https://www.zip-codes.com/'
county ='fort-bend'
#html_data = requests.get('https://www.zip-codes.com/county/tx-harris.asp')
html_data = requests.get('https://www.zip-codes.com/county/tx-'+county+'.asp')

html_content = html_data.content
soup = BeautifulSoup(html_content, 'html.parser')

#locate the table containing "HARRIS County, TX Covers 230 ZIP Codes"
tab_loc = soup.table.tr.find_all('td')[1].find_all('div')[0].find_all('table')[1]

links = []
#read links.
for row in tab_loc.find_all('tr'):
    try:
        links.append(row.a['href'])
    except:
        continue

link_len = len(links)

results_all =[]
for i, link in enumerate(links):
    url_zip = url + link
    print('Running links >>>  ' +str(i+1) +'/'+str(link_len))
    print(url_zip)

    html_zip_data = requests.get(url_zip)

    html_zip_content = html_zip_data.content
    soup = BeautifulSoup(html_zip_content, 'html.parser')

    #record the table titles.
    # titles = []
    # title_loc = soup.table.tr.find_all('td')[1].find_all('div')[0]
    # for title in title_loc.find_all('h2')[0:5]:
    #     titles.append(title.text)

    cols = []
    values = []
    tab_loc = soup.table.tr.find_all('td')[1].find_all('div')[0]
    tables  = tab_loc.find_all('table')

    #read first 3 tables.
    for tab in tables[0:3]:
        for row in tab.find_all('tr'):
            temp = row.text.split(':')
            if(temp[0] != 'City Alias(es) To Avoid Using'): #skip this row, only some zip codes area have.
                cols.append(temp[0])
                values.append(temp[1])

    #read 4th table.
    for tab in tables[3:4]:
        for row in tab.find_all('tr')[1:]:
            temp = row.text.strip().replace('\n',':').split(':')
            cols.append(temp[0]+'(2009)')
            values.append(temp[2])
            cols.append(temp[0]+'(2010)')
            values.append(temp[3])

    results_all.append(values)

result = pd.DataFrame(results_all, columns=cols)
#result.append(values, ignore_index=True)
#result.to_csv('HARRIS-County-Data.csv')
result.to_csv(county +'-County-Data.csv')


end_time = time.time()
elapse_time = round(end_time-start_time, 2)

print('finished. code ran for {} s.'.format(elapse_time))
