#!/usr/bin/env python
# coding: utf-8

# In[2]:


# from Erie County Sheriff's website:
# https://www2.erie.gov/sheriff/index.php?q=warrants

# Soma scraping review at 
# https://columbia.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=aeff3d16-0b3c-4ab7-a84c-ad5d0133d80b


# In[3]:


import requests
from bs4 import BeautifulSoup


# In[4]:


response = requests.get('https://www2.erie.gov/sheriff/index.php?q=warrants')
doc = BeautifulSoup(response.text, 'html.parser')


# In[5]:


# explanation of CSS selectors:
# .media_title means "something with the class of media_title"
# h3 means "something with the tag name of h3"
# h3.media_title means "something with the tag name of h3 AND the class of media_title"

# h3.media_title a
# means "a link inside of (an h3 tag with the class of media_title)"


# In[6]:


# get all the <td> tags with the class views-field-field-war-last-name-value
# could do it this way:
# doc.find_all('td', class_='views-field-field-war-last-name-value')

# but this is a better way:

doc.select('td.views-field-field-war-last-name-value a')


# In[8]:


suspects = doc.select('td.views-field-field-war-last-name-value a')

for suspect in suspects:
    print("--------------")
    print(suspect.text)


# In[9]:


addresses = doc.select('td.views-field-field-war-address-value')

for address in addresses:
    print("--------------")
    print(address.text)


# In[10]:


# <tr class_="odd views-row-first views-row-last">

suspects = doc.select('tr.odd')

for suspect in suspects:
    print("--------------")
    print(suspect.text)
    


# In[11]:


# <tr class_="odd views-row-first views-row-last">

suspects = doc.select('tr.odd')

for suspect in suspects:
    print("--------------")
   # print(suspect)
    print(suspect.select_one("td.views-field-field-war-last-name-value").text)
    print(suspect.select_one("td.views-field-field-war-address-value").text)
    print(suspect.select_one("td.views-field-field-war-description-value").text)
    print(suspect.select_one("span.date-display-single").text)
    print(suspect.select_one("td.views-field-field-war-cl-case-num-value").text.strip())
    print(suspect.select_one("td.views-field-field-war-reason-value").text.strip())
    


# In[13]:


suspects = doc.select('tr.odd')

for suspect in suspects:
    print("--------------")
    row = {}
    row['suspect_name'] = suspect.select_one("td.views-field-field-war-last-name-value").text
    row['last_known_address'] = suspect.select_one("td.views-field-field-war-address-value").text
    row['suspect_description'] = suspect.select_one("td.views-field-field-war-description-value").text
    row['date_received'] = suspect.select_one("span.date-display-single").text
    row['warrant_number'] = suspect.select_one("td.views-field-field-war-cl-case-num-value").text.strip()
    row['reason_for_warrant'] = suspect.select_one("td.views-field-field-war-reason-value").text.strip()
    print(row)


# In[30]:


suspects = doc.select('tr.odd')

rows = []

for suspect in suspects:
    print("--------------")
    row = {}
    
    row['suspect_name'] = suspect.select_one("td.views-field-field-war-last-name-value").text.strip()
    
    try:
        row['last_known_address'] = suspect.select_one("td.views-field-field-war-address-value").text.strip()
    except:
        print("Couldn't find an address")
        
    try:
        row['suspect_description'] = suspect.select_one("td.views-field-field-war-description-value").text.strip()
    except:
        print("Couldn't find a suspect description")
        
    try: 
        row['date_received'] = suspect.select_one("span.date-display-single").text.strip()
    except:
        print("Couldn't find a date received")
        
    try: 
        row['warrant_number'] = suspect.select_one("td.views-field-field-war-cl-case-num-value").text.strip()
    except:
        print("Couldn't find a warrant number")
        
    try:
        row['reason_for_warrant'] = suspect.select_one("td.views-field-field-war-reason-value").text.strip()
    except:
        print("Couldn't find a reason for warrant")
        
    print(row)
    
    rows.append(row)
    


# In[31]:


import pandas as pd


# In[32]:


df = pd.DataFrame(rows)
df


# In[33]:


df.to_csv("warrants.csv")


# In[ ]:





# In[ ]:




