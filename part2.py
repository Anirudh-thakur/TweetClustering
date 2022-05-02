# -*- coding: utf-8 -*-
"""part2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Msl_NDk1xExta79evw5uFCBIPIMPaI0S
"""

import pandas as pd
import re
from random import choice

def loadAndProcessData(filename):
    tweet_df = pd.read_csv(filename, sep="|", header=None, names=["ID", "TIMESTAMP", "TWEET"],encoding= 'unicode_escape')
    tweet_df.drop(['TIMESTAMP'], axis = 1, inplace = True)
    # Removing the links from the tweets 
    tweet_df['TWEET']=tweet_df['TWEET'].apply(lambda tweet : re.sub(r'https?://[^ ]+', '', tweet) )
    # Removing the username from the tweets 
    tweet_df['TWEET']=tweet_df['TWEET'].apply(lambda tweet : re.sub(r'@[^ ]+', '', tweet) )
    # Removing the # from the tweets 
    tweet_df['TWEET']=tweet_df['TWEET'].apply(lambda tweet : re.sub(r'#', '', tweet) )
    # Removing the special charaters and number
    tweet_df['TWEET']=tweet_df['TWEET'].apply(lambda tweet : re.sub(r'[^A-Za-z ]', '', tweet) )
    # Convert All the text to lowercase 
    tweet_df['TWEET']=tweet_df['TWEET'].apply(lambda tweet :  tweet.lower() )
    # Normalize the data 
    tweet_df['TWEET']=tweet_df['TWEET'].apply(lambda tweet : re.sub(r'([A-Za-z])\1{2,}', r'\1', tweet) )
    # remove rt which stands for re tweet 
    tweet_df['TWEET']=tweet_df['TWEET'].apply(lambda tweet : re.sub(r'^rt ', '', tweet) )
    #converting the tweet to set of words
    tweet_df['TWEET']=tweet_df['TWEET'].apply(lambda tweet: set(str(tweet).split()))
    return tweet_df

def getScore(oneTweet,twoTweet):
    inter = list(oneTweet & twoTweet)
    I = len(inter)
    union = list(oneTweet | twoTweet)
    U = len(union)
    return round(1 - (float(I) / U), 4)

def getIntialCenteriods(tweet_dic,k):
    tweet_score=[]
    for key in tweet_dic:
        currentScore=0
        for ele in tweet_dic:
            if key!=ele:
                currentScore+=getScore(tweet_dic[key],tweet_dic[ele])
        tweet_score.append([currentScore,key])
    tweet_score=sorted(tweet_score, key=lambda x: x[0])
    centeriods={}
    for i in range(int(len(tweet_score)/2-int(k/2)),int(len(tweet_score)/2)+int(k/2)+1):
        centeriods[tweet_score[i][1]]=[]
    return centeriods

def assignCluster(tweet_dic,centertiods):
    for tweet in tweet_dic:
        min_Tweet=[1.1,None]
        for center in centertiods:
            current=getScore(tweet_dic[tweet],tweet_dic[center])
            if current<min_Tweet[0]:
                min_Tweet=[current,center]
        centertiods[min_Tweet[1]].append(tweet)
    return centertiods

def oneCenter(listOfTweet):
    tweet_score=[]
    len_Tweet=len(listOfTweet)
    for key in listOfTweet:
        currentScore=0
        for ele in listOfTweet:
            if key!=ele:
                currentScore+=getScore(tweet_dic[key],tweet_dic[ele])
        tweet_score.append([currentScore,key])
    tweet_score=sorted(tweet_score, key=lambda x: x[0])
    return tweet_score[0][1]

def SSE(centeriods):
    distance=0
    for center in centeriods:
        for tweet in centeriods[center]:
            distance+=getScore(tweet_dic[center],tweet_dic[tweet])
    return round(distance,2)

#main
tweet=loadAndProcessData('usnewshealth.txt')
tweet_dic=dict(zip(tweet['ID'], tweet['TWEET']))
centeriods={}
k_Value=[5,10,15,20]
for k in k_Value:
    print("Value of K: {}".format(k))
    count=0
    while count<k:
        key=choice(list(tweet_dic.keys()))
        if key not in centeriods:
            centeriods[key]=[]
            count+=1
    #print(centeriods)
    #centeriods=getIntialCenteriods(tweet_dic,10)
    preCenteriods=set()
    currentCenteriods=set(centeriods.keys())
    centeriods=assignCluster(tweet_dic,centeriods)
    count=1
    while not(preCenteriods == currentCenteriods):
        #print(count)
        count+=1
        preCenteriods=currentCenteriods.copy()
        newCenteriods={}
        for center in centeriods:
            newCenter=oneCenter(centeriods[center])
            newCenteriods[newCenter]=[]
        newCenteriods=assignCluster(tweet_dic,newCenteriods)
        centeriods=newCenteriods.copy()
        currentCenteriods=set(centeriods.keys())
    count=0
    #print(centeriods)
    sse_value=SSE(centeriods)

    print("SSE value: {}".format(sse_value))
    for center in centeriods:
        count+=1
        print(" Size of cluster {} : {}".format(count,len(centeriods[center])))

