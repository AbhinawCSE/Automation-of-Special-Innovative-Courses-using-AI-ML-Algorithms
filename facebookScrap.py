#!/usr/bin/env python
# coding: utf-8

# # Facebook scraper
from facebook_scraper import get_posts
import datetime
import math
def facebookScraper(eventName,fbIdName):
    stoplists=[]
    stoplists += eventName.split()
    count=dict.fromkeys(stoplists, 0)
    totalWordsMatch=0
    count1=0
    sum=0
    for post in get_posts(fbIdName, pages=0):
        for word in stoplists:
            if word.lower() in post["text"].lower():
                count[word] += 1 
    totalWordsToMatch = len(count)
    # for word in count.keys():
    #     count[word]=count[word]*count[word]
    #     sum+=count[word]
    # avg=sum/totalWordsToMatch
    # sqrt = math.sqrt(avg)
    # return round(sqrt,2)
    for i in count:
        if count[i]!=0:
            totalWordsMatch+=1
    percentageOfMatch = totalWordsMatch/totalWordsToMatch
    return percentageOfMatch

if __name__ == '__main__':
    facebookScraper("innovation challenge 2018 2020","TheInnovationChallenge")

