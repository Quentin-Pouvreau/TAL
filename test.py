from twython import Twython


app_key="zjvCEgFYMsEaGAcGxGLBEsQHt"  
app_secret="Zcyao8oaRNmrJLFTzGmb0kXrnWEEgYcTqiJDQTRpI7lw8yGfnS"  
oauth_token="516790403-GRGsQKUIhtpLXmlTj6HQVR2oxw7VzzbvXy0JmbF0" 
oauth_token_secret="U6rxN7HE2lfnkWJ9zqCew3x52hlvKSkrIl7GvgsVtqZNx"



twitter = Twython(app_key , app_secret ,
                  oauth_token, oauth_token_secret)

results = twitter.cursor(twitter.search, q='twitter', tweet_mode='extended', lang='fr')
for result in results:
	rt = result['full_text']
	print (rt)
	print ("-------------------")



""" test"""
