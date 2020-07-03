#!/usr/bin/env python
# coding: utf-8

# # Web scraping from website

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# url = input('Enter - ')
# html = urlopen(url, context=ctx).read()
# soup = BeautifulSoup(html, "html.parser")

def webScraping(url,additional_words):
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # res = requests.get(url)
    # html_page = res.content
    html_page = urlopen(url, context=ctx).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    output = ''
    blacklist = ['[document]','noscript','header','html','meta','head', 'input','script','style','span','img','footer']
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    # save the scraped website into text file 
    file = open("C:/Users/Abhi/Desktop/Project20/webextract/webscrapping.txt","a",encoding="utf-8")
    file.write(output+"\n")
    file.close()
    # spliting the string into words
    stoplists=[]
    stoplists += additional_words.split()
    # create a dictionary for all search words, setting each count to 0
    count = dict.fromkeys(stoplists, 0)
    totalWordMatch=0
    # find the word in the text file and save that line in another file
    F1 = open('C:/Users/Abhi/Desktop/Project20/webextract/webscrapping1.txt', 'w',encoding="utf-8")
    with open('C:/Users/Abhi/Desktop/Project20/webextract/webscrapping.txt','r',encoding="utf-8") as f:
        for line in f:
            for word in stoplists:
                if word in line:
                    # found a word you wanted to count, so count it
                    count[word] += 1
                    F1.write("%s\n" %(line.lower()))
    f.close()
    F1.close()
    totalWordsToMatchLength=len(count)
    for i in count:
        if count[i]!=0:
            totalWordMatch+=1
    percentageOfMatch = totalWordMatch/totalWordsToMatchLength
    return percentageOfMatch  

if __name__ == '__main__':
    webScraping(input("Enter the url: "),input("Enter the string: "))