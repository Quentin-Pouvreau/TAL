# -*- coding: utf-8 -*-

import os
import tweepy
import re
import time
import smoothing
import semantic
import sys

app_key="zjvCEgFYMsEaGAcGxGLBEsQHt"  
app_secret="Zcyao8oaRNmrJLFTzGmb0kXrnWEEgYcTqiJDQTRpI7lw8yGfnS"  
oauth_token="516790403-GRGsQKUIhtpLXmlTj6HQVR2oxw7VzzbvXy0JmbF0" 
oauth_token_secret="U6rxN7HE2lfnkWJ9zqCew3x52hlvKSkrIl7GvgsVtqZNx"

auth = tweepy.OAuthHandler(app_key, app_secret)
auth.set_access_token(oauth_token, oauth_token_secret)
api = tweepy.API(auth)


def file_reader(fileNameTweets):
	with open(fileNameTweets, "r") as tweetReader:
		for readline in (tweetReader):
			#tweetReader.readline()
			print(readline)
			os.system("echo \" "+readline+"\" | MElt")


def process_status(status):
	for tweet in status:
		if "retweeted_status" in dir(tweet): 
			rt = tweet.retweeted_status.full_text
		else:
			rt = tweet.full_text
		print (tweet.user.screen_name)
		print (tweet.created_at)
		clean_tweet = re.sub(r"http\S+|@\S+|#\S+", "", rt)
		print (clean_tweet)


def building_learning_corpus():
	stream_tweets = tweepy.Cursor(api.search, q="* -filter:retweets", tweet_mode="extended", lang="fr").items(1000)
	file_name = "Corpus_Apprentissage/corpus_apprentissage_"+time.strftime('%d-%m-%Y')+"_"+time.strftime('%Ih%M')+".txt"
	apprentissage = open(file_name,"a",encoding="utf8")
	for tweet in stream_tweets:
		if "retweeted_status" in dir(tweet): 
			rt = tweet.retweeted_status.full_text
		else:
			rt = tweet.full_text
		clean_tweet = re.sub(r"http\S+|@\S+|#\S+", "", rt)
		apprentissage.write(clean_tweet+"\n")
	print("done")


def building_corpus(select):
	data = None 
	if select == "1":
		var = input("Entrez le nom de la victime que vous cherchez :")
		data = tweepy.Cursor(api.search, q="="+var+" -filter:retweets", tweet_mode="extended", lang="fr").items(500)
	elif select == "2":
		var = input("Entrez le nom d'utilisateur Twitter de l'agresseur que vous cherchez :")
		data = re.sub(r"@\S+","", str(var))
		data = tweepy.Cursor(api.user_timeline, "@"+str(var)+"", tweet_mode="extended").items(500)
	else:
		sys.exit("Mauvaise valeur") 

	file_name = "Corpus_Traitement/Corpus_de_"+str(var)+"_clean_"+time.strftime('%d-%m-%Y')+"_"+time.strftime('%Ih%M')+".txt"
	corpus = open(file_name,"a",encoding="utf8")
	for tweet in data:
		if "retweeted_status" in dir(tweet): 
			rt = rt = tweet.retweeted_status.full_text
		else:
			rt = tweet.full_text
		clean_tweet = re.sub(r"http\S+","", rt)
		clean_tweet = re.sub(r"#","", clean_tweet)
		corpus.write(clean_tweet+"\n")
	corpus.close()
	smoothing.correctCorpus(file_name)
	os.system("rm MEltedTweets.melt")
	os.system("rm badTweets.melt")
	os.system("cat correctedCorpus.txt | MElt -L -T >> MEltedTweets.melt")
	semantic.filterBadTweets("MEltedTweets.melt")
	os.system("grew -det -grs POStoSSQ/grs/surf_synt_main.grs -i badTweets.melt -f resultatgrew.conll")
	semantic.comfirmBadTweets("resultatgrew.conll")
