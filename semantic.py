# -*- coding: utf-8 -*-

import os
import re

badWordsTxt = open("dictionnaire_mot_cle.txt", 'r', encoding="utf8")
badWords = list()
for badWord in badWordsTxt:
    badWords.append(badWord.strip())
badWordsTxt.close()

def isBadTweet(meltedTweet):
    tokens = list()
    for token in meltedTweet.split(" "):
        tokens.append(token.split("/")[2])
    s = " "
    tweet = s.join(tokens)
    for badWord in badWords:
        if re.search(r"\s*{0}\s".format(badWord), tweet) is not None:
            return True
    return False

def prepar(grewtweet):
    w, h = 10, 280;
    matrixGrew = [[0 for x in range(w)] for y in range(h)] 
    i=0
    for line in grewTweet.split(" "):
        lineclean = line.strip("\n")
        listitems = lineclean.split("\t")
        y=0
        for item in listitems:
            matrixGrew[i][y] = item
            y+=1   
        i+=1
    return matrixGrew

def isNegation(grewTweet):
        assignementBadWord = ""
        assignementNegation = ""
    for z in range(len(matrixGrew)):
        if str(matrixGrew[z][1]) in badWords:
            if str(matrixGrew[z][7]) == "ats":
                assignementBadWord = matrixGrew[z][6]
                if assignementBadWord == "_":
                    return False
    for v in range(len(matrixGrew)):
        if str(matrixGrew[v][1]) in ("pas"): 
            assignementNegation = matrixGrew[v][6]
            if assignementNegation == "_":
                return False
            elif assignementBadWord == assignementNegation:
                if matrixGrew[int(assignementNegation)-1][2] in ("être", "consister", "demeurer", "devenir", "rester", "s'appeler", "sembler", "paraître"):
                    return True
    return False
''' voir les obj.p'''
def filterNegation(grewFile):
    grewTweets = open(grewFile, 'r', encoding="utf8")
    nonNegationTweets = open("nonNegationTweets.conll", 'w', encoding="utf8")
    negationTweets = open("negationTweets.conll", 'w', encoding="utf8")
    grewTweet = ""
    for line in grewTweets: 
        if not line.strip():
            if not isNegation(grewTweet):
                nonNegationTweets.write(grewTweet+"\n")
            elif isNegation(grewTweet):
                negationTweets.write(grewTweet+"\n")
            grewTweet = ""
        else:
            grewTweet = grewTweet+line+" \n"
    grewTweets.close()
    nonNegationTweets.close()
    negationTweets.close()


def filterBadTweets(meltedTweetsFile):
    meltedTweets = open(meltedTweetsFile, 'r', encoding="utf8")
    badTweets = open("badTweets.melt", 'w', encoding="utf8")
    for tweet in meltedTweets:
        if isBadTweet(tweet):
            badTweets.write(tweet)
    badTweets.close()
    meltedTweets.close()