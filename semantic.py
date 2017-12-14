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


def prepare(grewtweet):
    matrixGrew = list()
    for line in grewtweet.split(" "):
        matrixGrew.append(line.split("\t"))
    return matrixGrew

def isNegation(badWord, matrixGrew):
    assignementNegation = ""
    assignementBadWord = badWord[6]
    for token in matrixGrew:
        if token[1] == "pas":
            assignementNegation = token[6]
            if assignementBadWord == assignementNegation:
                return True
    return False

def comfirmBadTweets(grewFile):
    grewTweets = open(grewFile, 'r', encoding="utf8")
    nonNegationTweets = open("nonNegationTweets.conll", 'w', encoding="utf8")
    negationTweets = open("negationTweets.conll", 'w', encoding="utf8")
    grewTweet = ""
    for line in grewTweets: 
        if not line.strip():
            grewmatrice = prepare(grewTweet)
            if isConfirmedBadTweet(grewmatrice):
                tokens = list()
                for token in grewmatrice:
                    tokens.append(str(token[1]))
                s = " "
                grewTweet = s.join(tokens)
                negationTweets.write(grewTweet)
            else:
                tokens = list()
                for token in grewmatrice:
                    tokens.append(str(token[1]))
                s = " "
                grewTweet = s.join(tokens)
                nonNegationTweets.write(grewTweet)
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


def isConfirmedBadTweet(grewedTweet):
    '''grewedTweet is a tab which contains syntax analyze of tweet'''
    for token in grewedTweet:
        if token[2] in badWords:
            if token[7] == "_" or token[7] == "suj" or token[7] == "obj":
                return True
            elif token[7] == "ats":
                if not isNegation(token,grewedTweet) and isTargeted(token, grewedTweet):
                    return True
            elif token[7] == "mod":
                if isTargeted(token, grewedTweet):
                    return True

    return False


def isTargeted(badWord, grewedTweet):
    for token in grewedTweet:
        if token[6] == badWord[6] and token[2] != badWord[2]:
            if badWord[7] == "ats" and token[7] == "suj":
                if re.match(r"je|j'|nous|c'|ça|cela", token[1]) is not None:
                    return False
        if token[0] == badWord[6] and token[7] == "ats":
            return isTargeted(token, grewedTweet)
        elif token[0] == badWord[6] and token[7] == "suj" and token[3] == "N":
            for det in grewedTweet:
                if det[6] == token[0] and det[7] == "det" and det[2] == "un":
                    return False
    return True