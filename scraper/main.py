##!/usr/bin/env python
# coding: utf-8

# In[24]:


# run only when running the first time
# for dependency installation
import sys
# get_ipython().system('{sys.executable} -m pip install -r requirements.txt')
# get_ipython().system('{sys.executable} -m pip install chromedriver')

#import for date usage
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# In[34]:
import time
st = time.time()

# import for navigation
import time

import selenium
import webbrowser

from pyasn1.compat.octets import null
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
# import for reading/saving csv
import csv

##import for scraping
import requests
import certifi
from bs4 import BeautifulSoup as bs

import pandas as pd


# webbrowser.open('https://publicaccess.aylesburyvaledc.gov.uk/online-applications/')  # Go to example.com


# In[162]:


# opener
# change driver link accordingly
driver = webdriver.Chrome()

NAMES = ['wycombe', 'alyesburyvale', 'chilternandsouthbucks']
LINKS = ['https://publicaccess.wycombe.gov.uk/idoxpa-web/search.do?action=weeklyList',
             'https://publicaccess.aylesburyvaledc.gov.uk/online-applications/search.do?action=weeklyList',
             'https://pa.chilternandsouthbucks.gov.uk/online-applications/search.do?action=weeklyList'
             ]
urls = []
rows = []
dpl = []
data_dictionary = {}
def main():

    for index, i in enumerate(LINKS):
        urls.clear()
        rows.clear()
        dpl.clear()
        data_dictionary.clear()
        browser_controller(i, NAMES[index])

        # driver.get()
        # driver.get('    )
    driver.close()
    #et = time.time()
    #elapsed_time = et - st
    #res = et - st
    #final_res = res / 60
    #print('Execution time:', elapsed_time, 'seconds')
    #print('Execution time:', final_res, 'minutes')

    print('Scraping Done')


# In[37]:


##search_bar = driver.find_element_by_name("")


# In[174]:



# reading of each title
def read_data():
    # titles = driver.find_elements_by_css_selector("a")
    urls.append([titles.get_attribute("href") for titles in WebDriverWait(driver, 5).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "li.searchresult a")))])
    print(urls)


#
def no_results(to_check):
    to_check +='.do?action=firstPage'
    try:

        #'https://pa.chilternandsouthbucks.gov.uk/online-applications/weeklyListResults.do?action=firstPage'
        req5 = requests.get(to_check, verify=False)
        # soup = bs(html, parser='lxml')
        soup5 = bs(req5.text, 'html.parser')

        table = soup5.find('div', {'class': 'messagebox'})

        if (table.text):
            headers = []
            trs = table.find_all('li')
            return True



    except AttributeError:
        #print('Does not have Results yet')
        #print('Terminating the Program')
        return False
    except NameError:
        #print('Does not have Results yet')
        #print('Terminating the Program')
        return False
    except:
        #print('Does not have Results yet')
        #print('Terminating the Program')
        return False


#this method is used to add a new data in our dictionary
def add_to_dictionary(summary):
    index = len(data_dictionary)

    # for i in contacts:
    # summary.append(i)
    data_dictionary[index] = summary

def export(name):

    df = pd.DataFrame(list(data_dictionary.values()), index=data_dictionary.keys())
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y")
    stri =name +'_' + dt_string
    df.to_csv(stri + '.csv', index=False, encoding='utf-8')

# week beginning selection
# wait till load
def browser_controller(link, name):
    # browser open
    driver.get(link)

    # wait til load
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((driver.find_element_by_name('week'))))

    # filter set up
    sel = webdriver.support.select.Select(driver.find_element_by_name('week'))

    #selecting the first available week fromt he options
    sel.select_by_index(0)

    #ensuring that the Date Validated option is ticked
    validated_rb = driver.find_element_by_id('dateValidated')
    validated_rb.click()

    # clicking of search button
    search_btn = driver.find_element_by_css_selector('input.primary.recaptcha-submit')
    search_btn.click()

    #checking if there are results aready
    if (no_results(name)):
        # print('There is no data yet')
        sys.exit()

    while True:
        read_data()
        try:
            next_button = link = driver.find_element_by_link_text('Next')
            if (next_button.click()):
                print("success")

        except Exception:
            print("no  more next button")
            break

    # In[45]:

    # transfer of the scraped links from selenium
    print('rows here')
    rows = urls
    print(rows)

    # edit the headers
    #fields = ['Reference', 'Application Validated', 'Address', 'Proposal', 'Status', 'Email', 'Phone']

    # code for scraping
    for link in rows:
        for inner in link:
            iteration = 0

            URL = inner
            URL = URL.replace("[", "")
            URL = URL.replace("]", "")
            URL2 = URL.replace("summary", "contacts")
            req = requests.get(URL, verify=False)
            req2 = requests.get(URL2, verify=False)
            soup = bs(req.text, 'html.parser')
            soup2 = bs(req2.text, 'html.parser')
            # html = inner
            # soup = bs(html, parser='lxml')

            table = soup.find('table', {'id': 'simpleDetailsTable'})

            def rowgetDataText(tr, coltag):  # td (data) or th (header)

                return tr.find(coltag).get_text(strip=True)

            def rowgetHeaderText(tr, coltag):  # td (data) or th (header)

                return tr.find(coltag).get_text(strip=True)

            temp_dic = {}
            temp_key = ''
            temp_val = ''
            td = []
            headers = []
            trs = table.find_all('tr')
            table2 = soup2.find('table', {'class': 'agents'})
            # for summary scraping
            for index, tr in enumerate(trs):  # for every table row

                temp_key = rowgetHeaderText(tr, 'th')
                temp_val = rowgetDataText(tr, 'td')

                temp_dic[temp_key] = temp_val
            # if(column_count[index] == rowgetHeaderText(tr, 'th')):
            # temp_array[index] = rowgetDataText(tr, 'td')
            # temp_key = rowgetDataText(tr, 'td')
            # elif ( rowgetHeaderText(tr, 'th')  in column_count):
            # temp_array[column_count.index(rowgetHeaderText(tr, 'th'))] = rowgetDataText(tr, 'td')
            # else:
            # temp_array[index] =  'No Data'

            # for contacts scraping

            contact_data = []
            contact_headers = []

            table2 = soup2.find('table', {'class': 'agents'})
            try:
                if (table2.text):
                    contact_rows = table2.find_all('tr', {'class': 'row0'})

                    def get_indexOf(list, text):
                        for index, data in enumerate(list):  # for every table row
                            print(data.lower())
                            if (text.lower() in data.lower()):
                                return index
                            return null

                for index, tr in enumerate(contact_rows):  # for every table row

                    print(rowgetHeaderText(tr, 'th'))
                    print(rowgetDataText(tr, 'td'))

                    temp_key = rowgetHeaderText(tr, 'th')
                    temp_val = rowgetDataText(tr, 'td')

                    temp_dic[temp_key] = temp_val

                    # if ('mail' in rowgetDataText(tr, 'td') ):
                    # temp_array2[get_indexOf(column_count_additionals, 'email')] = rowgetDataText(tr, 'td')
                # elif(column_count_additionals[index] == rowgetHeaderText(tr, 'th')):
                # temp_array2[index] = rowgetDataText(tr, 'td')

                # elif ( rowgetHeaderText(tr, 'th')  in column_count_additionals):
                # temp_array2[column_count_additionals.index(rowgetHeaderText(tr, 'th'))] = rowgetDataText(tr, 'td')

                # elif ('phone' in rowgetHeaderText(tr, 'th') ):
                # temp_array2[get_indexOf(column_count_additionals, 'phone')] = rowgetDataText(tr, 'td')

                # else:
                # temp_array2[index] =  'No Data'

               # else:
                    #print('no dataaa')

            except NameError:
                print('Name Error')
            except:
                print('Does not have Agent')
            add_to_dictionary(temp_dic)
    print('Done Collecting Data')
    print('Exporting...')
    export(name)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
