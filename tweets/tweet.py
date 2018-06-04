from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API
from tweets import credentials
from time import sleep
from tweepy import TweepError


class TwitterClient:
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):

        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline,
                            id=self.twitter_user,
                            tweet_mode="extended").items(num_tweets):

            tweets.append(tweet.full_text)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []

        for friend in Cursor(self.twitter_client.friends,
                             id=self.twitter_user).items(num_friends):

            friend_list.append(friend)

        return friend_list

    def get_home_timeline_tweets(self, num_tweets):

        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline,
                            id=self.twitter_user).items(num_tweets):

            home_timeline_tweets.append(tweet)

        return home_timeline_tweets

    def retweet_tweet(self):

        for tweet in Cursor(self.twitter_client.search,
                            q=hashtag_list).items():

            try:
                tweet.retweet()
                print("Tweet re-tweeted")
                sleep(10)

            except TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    def save_tweet_in_file(self):

        for tweets in Cursor(self.twitter_client.search, q=hashtag_list,
                             since='2018-04-18', until='2018-04-19').items():

            try:
                # json.dumps(tweet)

                with open(tweets_filename, 'a') as tf:
                    tf.write(str(tweets))
                # sleep()

            except TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    def tweet_from_file(self, filename):

        with open(filename, 'r') as file:

            file_lines = file.readlines()

        for line in file_lines:

            try:
                print(line)
                if line != '\n':

                    self.twitter_client.update_status(line)
                    sleep(5)
                else:
                    pass
            except TweepError as e:
                print(e.reason)


class TwitterAuthenticator:
    """
    Twitter authenticator class
    """

    def authenticate_twitter_app(self):

        auth = OAuthHandler(credentials.CONSUMER_KEY,
                            credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN,
                              credentials.ACCESS_TOKEN_SECRET)

        return auth


class TwitterStreamer:

    """
    Class for streaming and processig live tweets
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):

        # this handles twitter authentication and the connection
        # to the twitter streaming api

        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filters twitter stream to capture data by keyword
        stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener):
    """
    This is a basics listener class that just prints to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, raw_data):
        try:
            print(raw_data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(raw_data)
            return True
        except BaseException as e:
            print("Error on Data: %s" % str(e))

    def on_error(self, status_code):
        if status_code == 420:
            # returning false on data method in case rate limit occurs
            return False
        print(status_code)


if __name__ == "__main__":

    twitter_profile = 'realDonaldTrump'
    # friends_file = "friends.json"
    hashtag_list = ["python"]
    tweets_filename = "streamed_tweets.json"
    
    # twitter_client = TwitterClient("kebbakanyi")
    # print(twitter_client.get_friend_list(10))
    # for friend in twitter_client.get_friend_list(10):
    #     print(friend.name, ' : ', friend.screen_name)

    # twitter_client = TwitterClient(twitter_profile)
    # for tweet in twitter_client.get_user_timeline_tweets(10):
    #     print(tweet, '\n')

    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(tweets_filename, hashtag_list)

    # retweeter = TwitterClient()
    # retweeter.retweet_tweet()

    # filename = 'good_timber.txt'
    # poem = TwitterClient()
    # poem.tweet_from_file(filename)

    # save_tweet = TwitterClient()
    # save_tweet.save_tweet_in_file()
