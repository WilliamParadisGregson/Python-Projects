ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET =""

from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import numpy as np
import pandas as pd
import sys

import mysql.connector
from datetime import datetime, timedelta
import requests
import requests
from bs4 import BeautifulSoup

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth

class TweetAnalyzer():

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        return df

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="crowddude"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM posts WHERE checked = 0")
myresult = mycursor.fetchall()
for row in myresult:
    ID=row[0]
    URL=row[7]
    if URL == "":
        getting_username = "SELECT * FROM influencers WHERE id = %s"
        mycursor.execute(getting_username, (ID,))
        myresult = mycursor.fetchall()
        for row in myresult:
            username = row[22]
            
        if __name__ == '__main__':

            twitter_client = TwitterClient()
            tweet_analyzer = TweetAnalyzer()

            api = twitter_client.get_twitter_client_api()
            tweets = api.user_timeline(screen_name=username, count=20)

            df = tweet_analyzer.tweets_to_data_frame(tweets)

            tweet_ID = np.array([tweet.id for tweet in tweets])
            tweet_ID = tweet_ID[0]
            
            dateb = np.array([tweet.created_at for tweet in tweets])
            date = datetime.today()
            
            def tweet_url(t):
                return "https://twitter.com/statuses/%s" % (tweet_ID)
            tweetURL = tweet_url(tweet_ID)
            
            updating_posturl = """UPDATE posts
                                SET post_url = %s
                                WHERE id = %s"""
            mycursor.execute(updating_posturl, (tweetURL, ID))
            updating_dates = """UPDATE posts
                                SET datetime = %s
                                WHERE id = %s"""
            mycursor.execute(updating_dates, (date, ID))
              
    else:
        getting_date = "SELECT * FROM posts WHERE id = %s"
        mycursor.execute(getting_date, (ID,))
        myresult = mycursor.fetchall()
        for row in myresult:
            Date = row[5]
            influencer_id = row[3]
        getting_username = "SELECT * FROM influencers WHERE id = %s"
        mycursor.execute(getting_username, (ID,))
        myresult = mycursor.fetchall()
        for row in myresult:
            username = row[22]
            
        if datetime.today() <= Date + timedelta(days=3):
            html = requests.get(URL)
            soup = BeautifulSoup(html.text, 'lxml')
            comment = soup.find_all('span', attrs={'class':'ProfileTweet-actionCountForAria'})[0].contents
            comment = [item.replace(" replies", "") for item in comment]
            comments = comment[0]
            
            tweet_ID = URL.split('/')[-1]
            
            if __name__ == '__main__':

                twitter_client = TwitterClient()
                tweet_analyzer = TweetAnalyzer()

                api = twitter_client.get_twitter_client_api()
                followers = api.get_user(username).followers_count
                
                tweets = api.statuses_lookup([tweet_ID])
                df1 = tweet_analyzer.tweets_to_data_frame(tweets)\

                likesb = np.array([tweet.favorite_count for tweet in tweets]) 
                likes = likesb[0]

                retweetb = np.array([tweet.retweet_count for tweet in tweets])
                retweet = retweetb[0]
                
                text = api.get_status(tweet_ID, tweet_mode='extended')._json['full_text']
                texxt = re.sub(r'http\S+', '', text)
                text2=texxt.split('#')[0]

                    
                updating_likes = """UPDATE posts
                                  SET likes = %s
                                    WHERE id = %s"""
                mycursor.execute(updating_likes, (int(likes), ID))

                updating_replies = """UPDATE posts
                                     SET comments = %s
                                       WHERE id = %s"""
                mycursor.execute(updating_replies, (int(comments), ID))

                updating_retweets = """UPDATE posts
                                       SET shares = %s
                                       WHERE id = %s"""
                mycursor.execute(updating_retweets, (int(retweet), ID))

                updating_checked = """UPDATE posts
                                     SET checked = %s
                                     WHERE id = %s"""
                mycursor.execute(updating_checked, (1, ID))

            getting_text = "SELECT * FROM campaigns WHERE id = %s"
            mycursor.execute(getting_date, (ID,))
            myresult = mycursor.fetchall()
            for row in myresult:
                tw_conditions = row[27]
                tw_formula = row [25]
                tw_formula_real = row [30]
                text1=row[22]
            
            sequence = difflib.SequenceMatcher(isjunk=None,a=str(text1),b=text2)
            difference = sequence.ratio()
            E = round(difference, 1)  
            C = int(comments)
            L = int(likes)
            F = followers
            R = int(retweet)
            
            if re.search('[f]+',tw_conditions):
                tw_conditions = tw_conditions.split('f')[-1]
                tw_conditions = int(tw_conditions)
                if followers > tw_conditions:
                    payout=tw_formula_real
                    change_brand_id=1
                else:
                    payout=tw_formula
                    change_brand_id=0
            else:
                payout=tw_formula
                change_brand_id=0
                tw_conditions = tw_conditions.split('p')[-1]
                tw_conditions = int(tw_conditions)
                if payout > tw_conditions:
                    payout=tw_formula_real
                    change_brand_id=1
                        
            if change_brand_id==1:
                updating_brand= """UPDATE financials 
                                     SET brand_id = -1 
                                     WHERE influencer_id = %s"""
                mycursor.execute(updating_brand, (influencer_id,))
                
            updating_balance= """UPDATE financials 
                                 SET balance = balance + %s 
                                 WHERE influencer_id = %s"""
            mycursor.execute(updating_balance, (payout, influencer_id))