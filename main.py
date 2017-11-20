import os
import tweepy
import re
import time


def file_reader(fileNameTweets):
	with open(fileNameTweets, "r") as tweetReader:
		for readline in (tweetReader):
			#tweetReader.readline()
			print(readline)
			os.system("echo \" "+readline+"\" | MElt")


app_key="zjvCEgFYMsEaGAcGxGLBEsQHt"  
app_secret="Zcyao8oaRNmrJLFTzGmb0kXrnWEEgYcTqiJDQTRpI7lw8yGfnS"  
oauth_token="516790403-GRGsQKUIhtpLXmlTj6HQVR2oxw7VzzbvXy0JmbF0" 
oauth_token_secret="U6rxN7HE2lfnkWJ9zqCew3x52hlvKSkrIl7GvgsVtqZNx"

auth = tweepy.OAuthHandler(app_key, app_secret)
auth.set_access_token(oauth_token, oauth_token_secret)

api = tweepy.API(auth)

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
	
		'''os.system("echo "+rt.encode('utf-8')+" | MElt -T >> test.txt")'''
		
def building_corpus(status):
	file_name = "corpus_apprentissage_"+time.strftime('%d:%m:%Y')+"_"+time.strftime('%Ih%M')+".txt"
	apprentissage = open(file_name,"a",encoding="utf8")
	for tweet in status:
		if "retweeted_status" in dir(tweet): 
			rt = tweet.retweeted_status.full_text
		else:
			rt = tweet.full_text
		clean_tweet = re.sub(r"http\S+|@\S+|#\S+", "", rt)
		apprentissage.write(clean_tweet+"\n")
		

def process_user(users):
	for user in users:
		print (user.name)
		print (user.description)
		print (user.location)


tweets_sample_by_name = tweepy.Cursor(api.search, q="emanuel macron from:piparkaq", tweet_mode="extended").items(3)
tweets_sample_by_location = tweepy.Cursor(api.search, q="Emmanuel Macron", geocode="48.692054,6.184417,50km", tweet_mode="extended", lang="fr").items(50)
tweets_sample_by_author = tweepy.Cursor(api.user_timeline, "@enjoyphenix", tweet_mode="extended").items(3)
targeted_tweet = tweepy.Cursor(api.search, q="EmmanuelMacron", tweet_mode="extended", lang="fr").items(100)
stream_tweets = tweepy.Cursor(api.search, q="*", tweet_mode="extended", lang="fr").items(1000)


building_corpus(stream_tweets)



