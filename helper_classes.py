import tweepy
import requests
import tensorflow_hub as hub
import random
import tensorflow as tf
import numpy as np
from PIL import Image
from utils import load_img, tensor_to_image

tf_hub = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'


class TwitterEngine:
    def __init__(self, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
                 TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET):
        self.TWITTER_CONSUMER_KEY = TWITTER_CONSUMER_KEY
        self.TWITTER_CONSUMER_SECRET = TWITTER_CONSUMER_SECRET
        self.TWITTER_ACCESS_TOKEN = TWITTER_ACCESS_TOKEN
        self.TWITTER_ACCESS_TOKEN_SECRET = TWITTER_ACCESS_TOKEN_SECRET
        self.auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,
                                        TWITTER_CONSUMER_SECRET)
        self.auth.set_access_token(TWITTER_ACCESS_TOKEN,
                                   TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

    def doTweet(self, tweet):
        try:
            self.api.update_status(status=tweet)
        except tweepy.TweepError as error:
            if error.api_code == 187:
                print('duplicate tweet')
            else:
                raise error
        return []

    def deleteLatestTweet(self):
        latestTweetId = self.api.user_timeline(count=1)[0].id_str
        self.api.destroy_status(latestTweetId)
        return []

    def doTweetWithMedia(self, tweet, img):
        try:
            media = self.api.media_upload(img)
            self.api.update_status(status=tweet, media_ids=[media.media_id])
        except tweepy.TweepError as error:
            if error.api_code == 187:
                print('duplicate tweet (with media)')
            else:
                raise error
        return []

class ArtEngine:
    def __init__(self, TRN_PEXELS_API_KEY):
        self.TRN_PEXELS_API_KEY = TRN_PEXELS_API_KEY
        self.hub_module = hub.load(tf_hub)

    def curateArt(self, topic, style):
        url = 'https://api.pexels.com/v1/search'
        per_page = '80'
        headers = {'Authorization': self.TRN_PEXELS_API_KEY}
        PARAMS = {'query': topic, 'per_page': per_page}
        r1 = (requests.get(url=url, params=PARAMS, headers=headers)).json()
        r2 = (requests.get(url=r1['next_page'], headers=headers)).json()
        photos = r1['photos'] + r2['photos']
        pic = random.choice(photos)
        image_path = pic['src']['original']
        img_data = requests.get(image_path).content
        with open('input_temp.jpg', 'wb') as handler:
            handler.write(img_data)

        content_img = load_img('input_temp.jpg')
        style_img = load_img('styles/' + style)
        out = self.hub_module(tf.constant(content_img),
                              tf.constant(style_img))[0]
        final_img = tensor_to_image(out)
        final_img.save('output_temp.png')
        return 'output_temp.png'


class NewsEngine:
    def __init__(self, NEWS_API_KEY):
        self.NEWS_API_KEY = NEWS_API_KEY

    def fetchNews(self, topic, pageSize):
        url = "https://newsapi.org/v2/everything?q=" + topic + \
            "&apiKey=" + self.NEWS_API_KEY + "&pageSize=" + str(pageSize)
        data = (requests.get(url=url)).json()

        # Formating data to be returned
        data = data['articles']
        return data
