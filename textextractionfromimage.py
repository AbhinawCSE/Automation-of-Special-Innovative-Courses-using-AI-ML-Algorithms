#!/usr/bin/env python
# coding: utf-8

# # Text extraction from certificate

import glob
import cv2
import pytesseract
import math
def textFromImage(imageName):
    image_list = []
    for filename in glob.glob(imageName): 
        im=cv2.imread(filename)
        image_list.append(im) 
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    texts = [pytesseract.image_to_string(img,lang = 'eng') for img in image_list]
    counter=0
    for text in texts:
        file = open('C:/Users/Abhi/Desktop/Project20/textextract/extractedText.txt','a')
        file.write('###')
        counter+=1
        file.write(str(counter))
        file.write('\n')
        file.write(text)
        file.write('\n')
        file.close() 

def textFromImage1(imageName):
    image_list = []
    for filename in glob.glob(imageName): 
        im=cv2.imread(filename)
        image_list.append(im) 
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    texts = [pytesseract.image_to_string(img,lang = 'eng') for img in image_list]
    counter=0
    for text in texts:
        file = open('C:/Users/Abhi/Desktop/Project20/textextract/extractedText1.txt','a')
        file.write('###')
        counter+=1
        file.write(str(counter))
        file.write('\n')
        file.write(text)
        file.write('\n')
        file.close() 
        
def searchingKeyWord(additional_words):
    #additional_words = "ramaiah university april 2018 jhjgfgx jhghfgy uytrter"
    sum=0
    outfile = 'C:/Users/Abhi/Desktop/Project20/textextract/extractedText.txt'
    stoplists=[]
    stoplists += additional_words.lower().split()
    # create a dictionary for all search words, setting each count to 0
    count = dict.fromkeys(stoplists, 0)
    totalWordsMatch=0
    with open(outfile, 'r') as f:
        for line in f:
            for word in line.lower().split():
                if word in stoplists:
                    # found a word you wanted to count, so count it
                    count[word] += 1
    f.close()
    totalWordsToMatch = len(count)
    # for word in count.keys():
    #     count[word]=count[word]*count[word]
    #     sum+=count[word]
    # avg=sum/totalWordsToMatch
    # sqrt = math.sqrt(avg)
    for i in count:
        if count[i]!=0:
            totalWordsMatch+=1
    percentageOfMatch = totalWordsMatch/totalWordsToMatch
    return percentageOfMatch
    # return round(sqrt,2)

def matchTwoFiles():
    f1 = open("C:/Users/Abhi/Desktop/Project20/textextract/extractedText.txt")
    f2 = open("C:/Users/Abhi/Desktop/Project20/textextract/extractedText1.txt")
    sum=0
    totalWordsMatch=0
    wordlist=[]
    for line in f2:
        wordlist.extend(line.lower().split())
    f2.close()
    worddict = dict.fromkeys(wordlist, 0)
    for line in f1:
        for word in wordlist:
            if word in line.lower():
                worddict[word]+=1
    f1.close()
    totalWordsToMatch = len(worddict)
    # for word in worddict.keys():
    #     worddict[word]=worddict[word]*worddict[word]
    #     sum+=worddict[word]
    # avg=sum/totalWordsToMatch
#     print("sum:",sum,"\ntotal Words",totalWordsToMatch,"\naverage:",avg,"\nsqrt",sqrt)
#     print("root mean square",round(sqrt,2))
    # return round(sqrt,2)
    for i in worddict:
        if worddict[i]!=0:
            totalWordsMatch+=1
    percentageOfMatch = totalWordsMatch/totalWordsToMatch
    return percentageOfMatch

if __name__ == '__main__':
    textFromImage(input("Enter the image: "))
    searchingKeyWord(input("Enter the Words to search: "))