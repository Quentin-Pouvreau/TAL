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