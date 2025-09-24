import pandas as pd
import json
import os
#from selenium import webdriver
#from selenium.webdriver.firefox.options import Options as FirefoxOptions
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By 
#from bs4 import BeautifulSoup
#import requests
import time
import random

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from nltk.corpus import gutenberg
from nltk.text import Text
import re

#load file
scrape=pd.read_csv('C:/Users/j-ste/Desktop/cali_final_scrape.csv')

#clean file
scrape['content2'].fillna('',inplace=True)
scrape['content_total']=scrape['content']+scrape['content2']

#scrape.at[0,'content_total'].concordance('sinclair')
scrape['content_s']=''
for row in scrape.index:
    temp=scrape.at[row,'content_total']
    temp_toke=word_tokenize(temp)
    scrape.at[row,'content_s']=nltk.Text(temp_toke)

#limit words to those around mentions of sinclair
scrape['con_list_sinc']=''
for row in scrape.index:
    temp=scrape.at[row,'content_s'].concordance_list('sinclair',width=200)
    scrape.at[row,'con_list_sinc']=temp


#test=scrape.at[0,'content_s'].concordance_list("sinclair",width=200)
#test[1].line
#combine contexualized language
scrape['con_list_sinc_text']=''
for row in scrape.index:
    i=0
    lis=[]
    temp=scrape.at[row,'con_list_sinc']
    while i < len(temp):
        #print(test[i].line)
        lis.append(temp[i].line)
        i+=1
    scrape.at[row,'con_list_sinc_text']=lis
    #len(test)

scrape['con_list_sinc_text2']=''
for row in scrape.index:
    scrape.at[row,'con_list_sinc_text2']=' '.join(scrape.at[row,'con_list_sinc_text'])

#format text for analysis    
scrape['text_final']=''
for row in scrape.index:
    temp=scrape.at[row,'con_list_sinc_text2']
    temp_toke=word_tokenize(temp)
    scrape.at[row,'text_final']=nltk.Text(temp_toke)


#define fuction to conduct sentiment analysis    
def add_vader_sentiment(df):
    sia = SentimentIntensityAnalyzer()
    df['vader_sentiment'] = df['con_list_sinc_text2'].apply(lambda x: sia.polarity_scores(x)['compound'])
    return df

#execute analysis and create final dataframe
df_final = add_vader_sentiment(scrape)
df_final2=df_final[['title','pageNumber','date','location','keywordMatches','url_article','post','con_list_sinc_text2',"vader_sentiment"]]

#output
df_final2.to_csv('C:/Users/j-ste/Desktop/sent_final.csv',index=False)
"""scrape2=scrape['vader_sentiment']
test=nltk.Text(scrape.at[0,'content_total'])
test.concordance('sinclair')

#corpus = gutenberg.words('melville-moby_dick.txt')
#text = Text(corpus)
#text.concordance("monstrous")
text= scrape2.at[0]
test=word_tokenize(text)
test2=nltk.Text(test)
list_test=test2.concordance_list('sinclair')

text="this is a test"
text_tok=word_tokenize(text)
test=nltk.Text(text_tok)

test2=nltk.corpus.gutenberg.words('melville-moby_dick.txt')
"""