import os


def filterBadTweets(tweets):
    tweets = open(tweets, 'r', encoding="utf8")
    badWordsTxt = open("dictionnaire_mot_cle.txt", 'r', encoding="utf8")
    badWords = list()
    for badWord in badWordsTxt:
        badWords.append(badWord)
    badTweets = open("badTweets.txt", 'w', encoding="utf8")
    for tweet in tweets:
        for badWord in badWords:
            if badWord in tweet.split(" "):
                badTweets.write(tweet)
                break
    badWordsTxt.close()
    badTweets.close()
    tweets.close()
    '''os.system("cat badTweets.txt | MElt -L -T > MEltedBadTweets.txt")'''


filterBadTweets("correctedCorpus.txt")