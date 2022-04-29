##!/usr/bin/env python
# coding: utf-8

# In[24]:


#run only when running the first time
#for dependency installation
import sys
#get_ipython().system('{sys.executable} -m pip install -r requirements.txt')
#get_ipython().system('{sys.executable} -m pip install chromedriver')


# In[34]:


#import for navigation
import time

import selenium
import webbrowser

from pyasn1.compat.octets import null
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
#import for reading/saving csv
import csv


##import for scraping
import requests
import certifi
from bs4 import BeautifulSoup as bs


# In[35]:




#webbrowser.open('https://publicaccess.aylesburyvaledc.gov.uk/online-applications/')  # Go to example.com


# In[162]:


#opener
#change driver link accordingly
driver = webdriver.Chrome()




def main():
    names = ['wycombe', 'alyesburyvale', 'chilternandsouthbucks']
    links = ['https://publicaccess.wycombe.gov.uk/idoxpa-web/search.do?action=weeklyList',
             'https://publicaccess.aylesburyvaledc.gov.uk/online-applications/search.do?action=weeklyList',
             'https://pa.chilternandsouthbucks.gov.uk/online-applications/search.do?action=weeklyList'
             ]
    for index, i in enumerate(links):
        browser_controller(i, names[index])

        #driver.get()
        #driver.get('    )
    driver.close()
    print('Scraping Done')

# In[37]:


##search_bar = driver.find_element_by_name("")


# In[174]:

urls = []
rows = []
dpl = []




#reading of each title
def read_data():
    #titles = driver.find_elements_by_css_selector("a")
    urls.append([titles.get_attribute("href") for titles in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "li.searchresult a")))])
    print(urls)



# In[161]:


#wait till the search results page is loaded

#list initialization and clear every run



#method for determining the final field labels to be used
def field_check(curr_list, new_list):
    print('curr')
    print(curr_list)

    print('new')
    print(new_list)
    if( len(curr_list) < len(new_list)):
        return new_list
    return curr_list


# In[70]:


#

def get_largest_field_count():


    count = 0

    field_container = ['']
    for link in urls:

        for inner in link:
            temp = []
            URL = inner
            URL = URL.replace("[", "")
            URL = URL.replace("]", "")
            req4 = requests.get(URL, verify=False)
            html = inner
                #soup = bs(html, parser='lxml')
            soup4 = bs(req4.text, 'html.parser')

            table = soup4.find('table', { 'id' : 'simpleDetailsTable' })

            def rowgetHeaderText(tr, coltag): # td (data) or th (header)
                return tr.find(coltag).get_text(strip=True)
            headers = []
            trs = table.find_all('tr')
            for tr in trs: # for every table row
                headers.append(rowgetHeaderText(tr, 'th') ) # data row


            field_container = field_check(field_container, headers )

    count = len(field_container)
    print('largest field count')
    print(field_container)
    return field_container

print('Compiled Successfully')


# In[118]:


#

def get_largest_field_count_contacts():


    count = 0

    field_container = ['']
    for link in urls:

        for inner in link:
            try:
                temp = []
                URL = inner
                URL = URL.replace("[", "")
                URL = URL.replace("]", "")
                URL = URL.replace("summary", "contacts")
                req = requests.get(URL, verify=False)
                html = inner
                    #soup = bs(html, parser='lxml')
                soup = bs(req.text, 'html.parser')

                table = soup.find('table', { 'class' : 'agents' })

                if(table.text):
                    def rowgetHeaderText(tr, coltag): # td (data) or th (header)
                        return tr.find(coltag).get_text(strip=True)
                    headers = []
                    trs = table.find_all('tr')
                    for tr in trs: # for every table row
                        headers.append(rowgetHeaderText(tr, 'th') ) # data row


                    field_container = field_check(field_container, headers )

            except AttributeError:
                print('nothing found')
            except NameError:
                print('Name Error')
            except:
                print('Does not have Agent')
    count = len(field_container)
    print('counting done')
    print(field_container)
    return field_container



#week beginning selection
#wait till load
def browser_controller(link, name):
    #browser open
    driver.get(link)

    #wait til load
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((driver.find_element_by_name ('week'))))

    # filter set up
    sel = webdriver.support.select.Select  (driver.find_element_by_name ('week'))
    sel.select_by_index(0)
    name2 = sel
    validated_rb = driver.find_element_by_id ('dateValidated')
    validated_rb.click()

    #clicking of search button
    search_btn =  driver.find_element_by_css_selector('input.primary.recaptcha-submit')
    search_btn.click()



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

    # In[4]:

    # In[5]:

    # In[21]:

    # edit the headers
    fields = ['Reference', 'Application Validated', 'Address', 'Proposal', 'Status', 'Email', 'Phone']

    # In[46]:
    column_count = get_largest_field_count()





    column_count_additionals = get_largest_field_count_contacts()







    field_indexes = [''] * len(column_count)
    #variables for the scraped data

    contacts_field_indexes =  [''] *  len(column_count_additionals)



    #code for scraping
    for link in rows:
        for inner in link:
            iteration = 0
            temp_array = ['No Data'] * len(column_count)
            temp_array2 = ['No Data'] * len(column_count_additionals)
            collect = []
            temp = []
            URL = inner
            URL = URL.replace("[", "")
            URL = URL.replace("]", "")


            URL2 = URL.replace("summary", "contacts")
            req = requests.get(URL, verify=False)
            req2 = requests.get(URL2, verify=False)
            soup = bs(req.text, 'html.parser')
            soup2 = bs(req2.text, 'html.parser')






            #html = inner
                #soup = bs(html, parser='lxml')


            table = soup.find('table', { 'id' : 'simpleDetailsTable' })


            def rowgetDataText(tr, coltag): # td (data) or th (header)

                return  tr.find(coltag).get_text(strip=True)

            def rowgetHeaderText(tr, coltag): # td (data) or th (header)

                return tr.find(coltag).get_text(strip=True)





            trs = table.find_all('tr')
            table2 = soup2.find('table', { 'class' : 'agents' })
            #for summary scraping
            print(column_count)
            for index, tr in enumerate(trs): # for every table row

                print(column_count[index])
                print(rowgetHeaderText(tr, 'th'))
                if(column_count[index] == rowgetHeaderText(tr, 'th')):
                    temp_array[index] = rowgetDataText(tr, 'td')

                elif ( rowgetHeaderText(tr, 'th')  in column_count):
                    temp_array[column_count.index(rowgetHeaderText(tr, 'th'))] = rowgetDataText(tr, 'td')
                else:
                    temp_array[index] =  'No Data'


           #for contacts scraping

            contact_data = []
            contact_headers = []



            table2 = soup2.find('table', { 'class' : 'agents' })
            try:
                if(table2.text):
                    contact_rows = table2.find_all('tr', { 'class' : 'row0' })
                    def get_indexOf(list, text):
                        for index, data in enumerate(list): # for every table row
                            print(data.lower())
                            if(text.lower() in data.lower()):
                                return index
                            return null

                for index, tr in enumerate(contact_rows): # for every table row

                    print(rowgetHeaderText(tr, 'th'))
                    print(rowgetDataText(tr, 'td'))

                    if ('mail' in rowgetDataText(tr, 'td') ):
                         temp_array2[get_indexOf(column_count_additionals, 'email')] = rowgetDataText(tr, 'td')
                    elif(column_count_additionals[index] == rowgetHeaderText(tr, 'th')):
                        temp_array2[index] = rowgetDataText(tr, 'td')

                    elif ( rowgetHeaderText(tr, 'th')  in column_count_additionals):
                        temp_array2[column_count_additionals.index(rowgetHeaderText(tr, 'th'))] = rowgetDataText(tr, 'td')

                    elif ('phone' in rowgetHeaderText(tr, 'th') ):
                         temp_array2[get_indexOf(column_count_additionals, 'phone')] = rowgetDataText(tr, 'td')


                    else:
                        temp_array2[index] =  'No Data'

                else:
                    print('no dataaa')

            except AttributeError:
                print('nothing found')
            except NameError:
                print('Name Error')
            except:
                print('Does not have Agent')


            # td.append(rowgetDataText(tr, 'td') ) # data row
            # headers.append(rowgetHeaderText(tr, 'th') ) # data row


            iteration += 1
            print('\nTemp Array2')
            print(temp_array2)
            dpl.append(temp_array + temp_array2)
    print('Done')




    #code for exporting
    with open( name+'_latest.csv', 'wt', newline='') as f:
        csv_writer = csv.writer(f)

        csv_writer.writerow(column_count + column_count_additionals)  # write header

        for row in dpl:
            csv_writer.writerow(row)
    print('csv exported')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
