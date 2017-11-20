import tweepy

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
		print (rt)
		print ("-------------------")
	'''print (api.rate_limit_status())'''


def process_user(users):
	for user in users:
		print (user.name)
		print (user.description)
		print (user.location)


tweets_sample_by_name = tweepy.Cursor(api.search, q="emanuel macron from:piparkaq", tweet_mode="extended").items(50)
tweets_sample_by_location = tweepy.Cursor(api.search, q="Emmanuel Macron", geocode="48.692054,6.184417,50km", tweet_mode="extended", lang="fr").items(50)


tweets_sample_by_author = tweepy.Cursor(api.user_timeline, "@piparkaq", tweet_mode="extended").items(50)

targeted_tweet = tweepy.Cursor(api.search, q="EmmanuelMacron", tweet_mode="extended", lang="fr").items(50)

process_status(tweets_sample_by_author)

'''
API.exists_friendship(user_a, user_b) -> Retourne un boolean pour savoir si oui ou non deux utilisateur se suivent
API.show_friendship(source_id/source_screen_name, target_id/target_screen_name) -> Donne des information a propos de cette relation
Tweeter API permet de gérer les status de block/spam des utlilisateurs
L'api permet aussi d'avoir des information assez pezcise sur la gealocalisation.
Limitation de l'api tweeter, pas de tweet plus vieux qu'une semaine. 
Possible solution :
	https://github.com/Jefferson-Henrique/GetOldTweets-python

	Retrouver des converstions sur tweeter :
	https://stackoverflow.com/questions/29928638/getting-tweet-replies-to-a-particular-tweet-from-a-particular-user
'''









   



