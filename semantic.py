# -*- coding: utf-8 -*-

import re

badWordsTxt = open("dictionnaire_mot_cle_non_interpretable.txt", 'r', encoding="utf8")
badWords = list()
for badWord in badWordsTxt:
    badWords.append(badWord.strip())
badWordsTxt.close()

interpretableBadWordsTxt = open("dictionnaire_mot_cles_interpretable.txt", 'r', encoding="utf8")
interpretableBadWords = list()
for interpretableBadWord in interpretableBadWordsTxt:
    interpretableBadWords.append(interpretableBadWord)
interpretableBadWordsTxt.close()


def getMEltedTokens(meltedTweet, index):
    tokens = list()
    for token in meltedTweet.split(" "):
        tokens.append(token.split("/")[index])
    s = " "
    return s.join(tokens)


def isBadTweet(meltedTweet):
    tweet = getMEltedTokens(meltedTweet, 2)
    for badWord in badWords:
        if re.search(r"\s*{0}\s".format(badWord), tweet) is not None:
            return True
    return False

def prepare(grewtweet):
    matrixGrew = list()
    for line in grewtweet.split(" "):
        if line != "\n":
            matrixGrew.append(line.strip().split("\t"))
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

def getGrewedToken(grewmatrice):
    tokens = list()
    for token in grewmatrice:
        tokens.append(token[1])
    s = " "
    return s.join(tokens)

def comfirmBadTweets(grewFile):
    grewTweets = open(grewFile, 'r', encoding="utf8")
    infirmedBadTweets = open("infirmedBadTweets.txt", 'w', encoding="utf8")
    confirmedBadTweets = open("confirmedBadTweets.txt", 'w', encoding="utf8")
    grewTweet = ""
    for line in grewTweets:
        if not line.strip():
            grewmatrice = prepare(grewTweet)
            if isConfirmedBadTweet(grewmatrice):
                grewTweet = getGrewedToken(grewmatrice)
                confirmedBadTweets.write(grewTweet+"\n")
            else:
                grewTweet = getGrewedToken(grewmatrice)
                infirmedBadTweets.write(grewTweet+"\n")
            grewTweet = ""
        else:
            grewTweet = grewTweet+line+" \n"
    grewTweets.close()
    infirmedBadTweets.close()
    confirmedBadTweets.close()


def canBeBadTweet(meltedTweet):
    tweet = getMEltedTokens(meltedTweet, 2)
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
            tweet = getMEltedTokens(tweet, 0)
            interpretableBadTweets.write(tweet)
    badTweets.close()
    meltedTweets.close()
    interpretableBadTweets.close()


def isConfirmedBadTweet(grewedTweet):
    '''grewedTweet is a tab which contains syntax analyze of tweet'''
    for token in grewedTweet:
        if isBadWord(token, grewedTweet):
            if token[7] == "_" or token[7] == "suj" or token[7] == "obj":
                return True
            elif token[7] == "ats":
                if not isNegation(token,grewedTweet) and isTargeted(token, grewedTweet):
                    return True
            elif token[7] == "mod":
                if isTargeted(token, grewedTweet):
                    return True
    return False


def isBadWord(token, grewedTweet):
    for badWord in badWords:
        if " " in badWord:
            i = -1
            confirmed = True
            for word in badWord.split(" "):
                if re.search(word, grewedTweet[int(token[0]) + i][2]) is not None:
                    i += 1
                else:
                    confirmed = False
                    break
            if confirmed:
                return True
        elif token[2] == badWord:
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