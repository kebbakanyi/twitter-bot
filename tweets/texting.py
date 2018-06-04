import requests
import tweets
import tweepy
import json

from twilio.rest import Client
import credentials


# client = Client(credentials.account_sid, credentials.auth_token)

# message = client.messages.create(
#     body='Hello there!',
#     from_='+12068006901',
#     to=''
# )

# print(message.sid)


# twitter_client = tweets.TwitterClient('kebbakanyi')
# # print(twitter_client.get_friend_list(10))
# for friend in twitter_client.get_friend_list(10):
#     print(friend.name, ' : ', friend.screen_name)



# twitter_streamer = tweets.TwitterStreamer()
# twitter_streamer.stream_tweets(tweets_filename, hashtag_list)

with open(tweets_filename, 'r+', encoding="utf-8") as file:

    json_data = json.load(file)
