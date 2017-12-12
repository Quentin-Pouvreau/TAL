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
	stream_tweets = tweepy.Cursor(api.search, q="*", tweet_mode="extended", lang="fr").items(1000)

	file_name = "Corpus_Apprentissage/corpus_apprentissage_"+time.strftime('%d-%m-%Y')+"_"+time.strftime('%Ih%M')+".txt"
	apprentissage = open(file_name,"a",encoding="utf8")
	for tweet in stream_tweets:
		if "retweeted_status" in dir(tweet): 
			rt = tweet.retweeted_status.full_text
		else:
			rt = tweet.full_text
		clean_tweet = re.sub(r"http\S+|@\S+|#\S+", "", rt)
		apprentissage.write(clean_tweet+"\n")

def building_corpus(select):
	data = None 
	var = input("Please enter the name of the persone you're looking for: ")
	if select == "1":
		data = tweepy.Cursor(api.search, q=str(var), tweet_mode="extended", lang="fr").items(10)
	else:
		data = tweepy.Cursor(api.user_timeline, "@"+str(var)+"", tweet_mode="extended").items(10)

	file_name = "Corpus_Traitement/Corpus_de_traintement_"+time.strftime('%d-%m-%Y')+"_"+time.strftime('%Ih%M')+".txt"
	apprentissage = open(file_name,"a",encoding="utf8")
	for tweet in data:
		if "retweeted_status" in dir(tweet): 
			rt = tweet.retweeted_status.full_text
		else:
			rt = tweet.full_text
		clean_tweet = re.sub(r"http\S+","", rt)
		apprentissage.write(str(tweet.user.screen_name)+"\nle "+str(tweet.created_at)+" a dit :\n"+clean_tweet+"\n"+"------"+"\n")


def process_user(users):
	for user in users:
		print (user.name)
		print (user.description)
		print (user.location)

tweets_sample_by_location = tweepy.Cursor(api.search, q="Emmanuel Macron", geocode="48.692054,6.184417,50km", tweet_mode="extended", lang="fr").items(50)

mode = input("Que shouaitez-vous faire : \n - Crée un corpus d'apprentissage: tapé 1 \n -Faire une recherge sur le harcèlement: tapé 2 \n")

if mode == 1:
	building_learning_corpus()
else:
	select = input("Votre recherge porte sur : \n -Une victime, tapé 1 \n -Un agresseur, tapé 2 \n")
	building_corpus(select)

	




'''tweets_sample_by_name = tweepy.Cursor(api.search, q="emanuel macron from:piparkaq", tweet_mode="extended").items()'''





