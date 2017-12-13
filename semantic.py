# -*- coding: utf-8 -*-

import os
import re

badWordsTxt = open("dictionnaire_mot_cle.txt", 'r', encoding="utf8")
badWords = list()
for badWord in badWordsTxt:
    badWords.append(badWord.strip())
badWordsTxt.close()

def isBadTweet(tweetmelte):
    tokens = list()
    for token in tweetmelte.split(" "):
        tokens.append(token.split("/")[2])
    s = " "
    tweet = s.join(tokens)
    for badWord in badWords:
        if re.search(r" {0} ".format(badWord), tweet) is not None:
            return True
    return False


def filterBadTweets(tweets):
    tweets = open(tweets, 'r', encoding="utf8")
    badTweets = open("badTweets.txt", 'w', encoding="utf8")
    for tweet in tweets:
        if isBadTweet(tweet):
            badTweets.write(tweet)
    badTweets.close()
    tweets.close()