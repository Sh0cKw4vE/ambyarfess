import tweepy
import constants
import time
import _json
from requests_oauthlib import  OAuth1
import requests
import os
import re

class Twitter:
    def __init__(self):
        print("Initializing Twitter...")
        self.inits = tweepy.OAuthHandler(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
        self.inits.set_access_token(constants.ACCESS_KEY, constants.ACCESS_SECRET)
        self.api = tweepy.API(self.inits)

    def read_dm(self):
        print("Get Direct Messages...")
        dms=list()
        try:
            api=self.api
            dm = api.list_direct_messages()
            for x in range(len(dm)):
                sender_id=dm[x].message_create['sender_id']
                message = dm[x].message_create['message_data']['text']
                message_data= str(dm[x].message_create['message_data'])
                json_data= _json.encode_basestring(message_data)

                print("Getting message -> "+str(message)+" by sender id "+str(sender_id))

                if "attachment" not in json_data:
                    print("DM doesnt have any media")
                    d = dict(message=message, sender_id=sender_id, id=dm[x].id, media = None)
                    dms.append(d)
                    dms.reverse()
                else:
                    print("DM have an attachment")
                    attachment = dm[x].message_create['message_data']['attachment']
                    d = dict(message = message, sender_id = sender_id, id= dm[x].id, media = attachment['media']['media_url'])
                    dms.append(d)
                    dms.reverse()

            print(str(len(dms))+" collected")
            time.sleep(60)
            return dms

        except Exception as ex:
            print("Error read in here")
            print(ex)
            time.sleep(60)
            pass

    def delete_dm(self, id):
        print("Deleteing dm with id = "+str(id))
        try:
            self.api.destroy_direct_message(id)
            time.sleep(40)
        except Exception as ex:
            print(ex)
            time.sleep(40)
            pass

    def post_tweet(self, tweet, id):
        try:
            self.api.update_status(tweet)
            time.sleep(40)
        except Exception as ex:
            print("Error Post in here")
            print(ex)
            time.sleep(40)
            pass

    def post_tweet_with_media(self, tweet, media_url):
        try:
            print("Downloading media...")
            arr = str(media_url).split('/')
            auth = OAuth1(client_key=constants.CONSUMER_KEY,
                          client_secret=constants.CONSUMER_SECRET,
                          resource_owner_secret=constants.ACCESS_SECRET,
                          resource_owner_key=constants.ACCESS_KEY)

            r = requests.get(media_url, auth = auth)
            with open(arr[9], 'wb') as f:
                f.write(r.content)
            print("Media downloaded successfully!")
            pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
            #pattern.sub("", str(tweet))
            #tweet = tweet.replace("https://", "")
            #tweet=tweet.sub(r"http\S+", "", str(tweet))
            mediasource = pattern.findall(tweet)
            #tweet=pattern.sub('',tweet)
            print(mediasource[len(mediasource)-1])
            tweet = tweet.replace(mediasource[len(mediasource)-1], "")
            print(tweet)
            self.api.update_with_media(filename= arr[9], status=tweet)
            os.remove(arr[9])
            print("Upload with media success")
        except Exception as ex:
            print("Error Post w/ Media in here")
            print(ex)
            time.sleep(40)
            pass