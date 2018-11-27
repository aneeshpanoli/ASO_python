import play_scraper
from bs4 import BeautifulSoup as bs
import os
import urllib, re
import pandas as pd
import time, datetime
import collections


def ScrapDetails():
    term = input("Please enter the play store search term: ")
    noofaps = input("Enter number of apps to analyse: ")
    appDetails = play_scraper.search(term, page=2)
    apId = []
    soupData =[]
    noofaps = int(noofaps)
    for i in appDetails:
        print(i['app_id']);
        apId.append("https://play.google.com/store/apps/details?id="+i['app_id'])
    if len(apId) < noofaps:
        noofaps = len(apId)
    for i in apId[:noofaps]:
        with urllib.request.urlopen(i) as f:
            soup = bs(f, 'lxml')
            soupData+= soup.findAll('meta')
    output_file = open("wordJumble.txt", 'wb')
    for i in soupData:
        if "google-site" not in str(i) and "robots" not in str(i) and "og:url" not in str(i) and "IE=10" not in str(i) and "og:type" not in str(i):
            line = str(i)+"\n"
            output_file.write(line.encode('utf-8'))
def PrintKeyWordSummary():
    wordCountDict1 = {}
    wordCountDict2 = {}
    cleanDict = {}
    with open("wordJumble.txt") as f:
        words = f.read()
    wordsList = re.findall(r"[\w']+", words)
    cleanWordList = []
    for i in wordsList:
        i = i.lower()
        if len(i) > 1:
            if i[-2:] == "es":
                i = i[:-1]
                if "content=" in i:
                    isplit = i.split('"')
                    for j in isplit:
                        cleanWordList.append(j)
        cleanWordList.append(i)
    for i in cleanWordList:
        if i not in wordCountDict1:
            wordCountDict1[i] = 1
        else:
            wordCountDict1[i] = wordCountDict1[i] +1
    #counts = collections.Counter(cleanWordList).most_common()


    # for i in counts:
    #     print(i)
    print("\n +++++++++++++++++++++++++++++++++++++++++\n")
    cleanDict = {}
    with open("wordJumble.txt") as f:
        words = f.read()
    wordsList = re.findall(r"[\w']+", words)
    cleanWordList = []
    for i in wordsList:
        i = i.lower()
        if len(i) > 1:
            if i[-2:] == "es":
                i = i[:-1]
                if "content=" in i:
                    isplit = i.split('"')
                    for j in isplit:
                        cleanWordList.append(j)
        cleanWordList.append(i)
    for i in cleanWordList:
        if i not in wordCountDict2:
            wordCountDict2[i] = 1
        else:
            wordCountDict2[i] = wordCountDict2[i] +1
    #counts = collections.Counter(cleanWordList).most_common()
    # for key, value in sorted(wordCountDict1.items(), key=lambda x: x[1], reverse=True):
    #     print(key +": "+str(value/20))
    # for key, value in sorted(wordCountDict2.items(), key=lambda x: x[1], reverse=True):
    #     print(key +": "+str(value))
    for key, value in sorted(wordCountDict1.items(), key=lambda x: x[1], reverse=True):
        if key in wordCountDict2:
            print(key+": "+str(value/20)+", "+ str(wordCountDict2[key]))
    for key, value in wordCountDict1.items():
        if key not in wordCountDict2:
            print(key)
def CountWordsInText():
    with open("wordJumble.txt") as f:
        words = f.read()
    wordsList = re.findall(r"[\w']+", words)
    counts = collections.Counter(wordsList).most_common(100)
    for i in counts:
        print (i)
def Main():
    mode = input("1 for data download, 2 for summary/comparison, 3 for word count: ")
    if mode == "1":
        ScrapDetails()
    elif mode == "2":
        PrintKeyWordSummary()
    elif mode == "3":
        CountWordsInText()
Main()
#CountWordsInText()
