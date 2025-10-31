import pandas as pd
import json
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from bs4 import BeautifulSoup
import requests
import time
import random

#FOR THIS CODE I COMMONLY UTILIZE FILE PATHS UNIQUE TO MY SYSTEM 
#ALL FILE PATHS MUST BE UPDATED EACH USE OF THIS CODE TO SUITE THE UNIQUE FILE PATH OF THE USER

#select newspaper.com as our main website
base="https://www.newspapers.com"

#test opening json file which is what the scrape is saved as
#this ensures json files are loading properly before loading them all
f=open('C:/Users/j-ste/Desktop/Cali_Election_1934_Research/output-post/article_1755553201575.json')
data=json.load(f)

#establish dataframe by taking in first json, then transposing, assigning column headers and then clearing,
# do for both dataframes pre and post
post=pd.DataFrame(data.items())
post=post.transpose()
post.columns=post.iloc[0]
post=post.iloc[:0]
pre=post.iloc[:0]

#pull info from json files and put into dataframe (since i used diff in diff, seperated pulls into pre and post query)
directory='C:/Users/j-ste/Desktop/Cali_Election_1934_Research/output-post/'

for name in os.listdir(directory):
    fil=open(os.path.join(directory, name))
    data_fil=json.load(fil)
    post.loc[len(post)]=[data_fil['title'],data_fil['pageNumber'],data_fil['date'],data_fil['location'],
                         data_fil['keywordMatches'],data_fil['url']]
    
#post['url_article']=post['url'].str.split('?')
post['url_article']=''
for row in post.index:
    post.at[row,'url_article']=post.at[row,'url'].split('?')[0]

for row in post.index:
    post.at[row,'url_article']=post.at[row,'url_article'].replace('image','newspage')+'/'

#edit data frame to extract unique article url to be used in scrape
post['url_article']=''
for row in post.index:
    post.at[row,'url_article']=base+post.at[row,'url'].split('?')[0]

for row in post.index:
    post.at[row,'url_article']=post.at[row,'url_article'].replace('image','newspage')

#delete duplicates
post=post.drop_duplicates(subset='url_article',keep='first')
    
post['content']=''





#iniate driver
driver=webdriver.Firefox()
#driver = webdriver.Firefox(executable_path=r'C:\Users\j-ste\Downloads\geckodriver.exe')
#driver.get("http://www.python.org") 

#loop through dataframe to open each url and then extract OCR from each webpage
for row in post.index:
    temp_URL=post.at[row,'url_article']
    driver.get(temp_URL)
    button=driver.find_element(By.CLASS_NAME,'TextLink.OCR_OCRToggle__o3hbt')
    time.sleep(random.random()*10)
    button.click()
    test=driver.find_element(By.CLASS_NAME,'OCR_OCRText__ONwPS.OCR_show__o5PFJ').text
    post.at[row,'content']=test
    time.sleep(random.random()*10)
#close driver
driver.quit()

#export results dataframe as csv
post.to_csv('C:/Users/j-ste/Desktop/cali_final_scrape_post.csv')

#now repeat previous steps for pre search criteria scrape
directory_pre='C:/Users/j-ste/Desktop/Cali_Election_1934_Research/output-pre/'

#pre=pre.drop(columns=['url_article','content'])
for name in os.listdir(directory_pre):
    fil=open(os.path.join(directory_pre, name))
    data_fil=json.load(fil)
    pre.loc[len(pre)]=[data_fil['title'],data_fil['pageNumber'],data_fil['date'],data_fil['location'],
                         data_fil['keywordMatches'],data_fil['url']]
    
#post['url_article']=post['url'].str.split('?')
pre['url_article']=''
for row in pre.index:
    pre.at[row,'url_article']=pre.at[row,'url'].split('?')[0]

for row in pre.index:
    pre.at[row,'url_article']=pre.at[row,'url_article'].replace('image','newspage')+'/'

pre['content']=''

pre['url_article']=''
for row in pre.index:
    pre.at[row,'url_article']=base+pre.at[row,'url'].split('?')[0]

for row in pre.index:
    pre.at[row,'url_article']=pre.at[row,'url_article'].replace('image','newspage')

#delete duplicates
pre=pre.drop_duplicates(subset='url_article',keep='first')
    
pre['content']=''

#iniate scrape for pre criteria scrape
driver=webdriver.Firefox()
#driver = webdriver.Firefox(executable_path=r'C:\Users\j-ste\Downloads\geckodriver.exe')
#driver.get("http://www.python.org") 
for row in pre.index:
    temp_URL=pre.at[row,'url_article']
    driver.get(temp_URL)
    button=driver.find_element(By.CLASS_NAME,'TextLink.OCR_OCRToggle__o3hbt')
    time.sleep(random.random()*10)
    button.click()
    test=driver.find_element(By.CLASS_NAME,'OCR_OCRText__ONwPS.OCR_show__o5PFJ').text
    pre.at[row,'content']=test
    time.sleep(random.random()*10)
driver.quit()

#export results as csv
pre.to_csv('C:/Users/j-ste/Desktop/cali_final_scrape_pre.csv')

#combine both dataframes into singular dataframe and denote which is pre and which is post dataframe
post['post']=1
pre['post']=0
final=pd.concat([pre,post])
#export final dataframe
final.to_csv('C:/Users/j-ste/Desktop/cali_final_scrape.csv')
