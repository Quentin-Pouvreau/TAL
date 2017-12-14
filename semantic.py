# -*- coding: utf-8 -*-

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


def filterBadTweets(meltedTweetsFile):
    meltedTweets = open(meltedTweetsFile, 'r', encoding="utf8")
    badTweets = open("badTweets.melt", 'w', encoding="utf8")
    for tweet in meltedTweets:
        if isBadTweet(tweet):
            badTweets.write(tweet)
    badTweets.close()
    meltedTweets.close()
