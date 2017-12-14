# -*- coding: utf-8 -*-

import re

badWordsTxt = open("dictionnaire_mot_cle_non_interpretable.txt", 'r', encoding="utf8")
badWords = list()
interpretableBadWordsTxt = open("dictionnaire_mot_cles_interpretable.txt", 'r', encoding="utf8")
interpretableBadWords = list()
for badWord in badWordsTxt:
    badWords.append(badWord.strip())
badWordsTxt.close()
for interpretableBadWord in interpretableBadWordsTxt:
    interpretableBadWords.append(interpretableBadWord)
interpretableBadWordsTxt.close()


def getTokens(meltedTweet, index):
    tokens = list()
    for token in meltedTweet.split(" "):
        tokens.append(token.split("/")[index])
    s = " "
    return s.join(tokens)


def isBadTweet(meltedTweet):
    tweet = getTokens(meltedTweet, 2)
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


def canBeBadTweet(meltedTweet):
    tweet = getTokens(meltedTweet, 2)
    for badWord in interpretableBadWords:
        if re.search(r"\s*{0}\s".format(badWord), tweet) is not None:
            return True
    return False


def filterBadTweets(meltedTweetsFile):
    meltedTweets = open(meltedTweetsFile, 'r', encoding="utf8")
    badTweets = open("badTweets.melt", 'w', encoding="utf8")
    interpretableBadTweets = open("interpretableBadTweets.txt", 'w', encoding="utf8")
    for tweet in meltedTweets:
        if isBadTweet(tweet):
            badTweets.write(tweet)
        elif canBeBadTweet(tweet):
            tweet = getTokens(tweet, 0)
            interpretableBadTweets.write(tweet)
    badTweets.close()
    meltedTweets.close()
    interpretableBadTweets.close()


def confirmBadTweet(grewedTweet):
    '''grewedTweet is a tab which contains syntax analyze of tweet'''
    for token in grewedTweet:
        if token[2] in badWords:
            if token[7] == "ats" or token[7] == "mod":
                if isNotTargeted(token, grewedTweet):
                    return False
            elif token[7] == "_":
                return True
            elif token[7] == "suj":
                return True
            elif token[7] == "obj":
                return True
    return False


def isNotTargeted(badWord, grewedTweet):
    for token in grewedTweet:
        if token[6] == badWord[6] and token[2] != badWord[2]:
            if badWord[7] == "ats" and token[7] == "suj":
                if re.match(r"je|j'|nous|c'|ça|cela", token[1]) is not None:
                    return True
        if token[0] == badWord[6] and token[7] == "ats":
            return isNotTargeted(token, grewedTweet)
        elif token[0] == badWord[6] and token[7] == "suj" and token[3] == "N":
            for det in grewedTweet:
                if det[6] == token[0] and det[7] == "det" and det[2] == "un":
                    return True
    return False