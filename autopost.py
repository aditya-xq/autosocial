import sys
sys.path.append("C:/Users/adity/Desktop/confidential")
from global_constants import *
from helper_classes import *
from utils import generateNewsTweet
import time
import random

#%%

tweet_art = '''Created via neural style transfer. Stock input from #pexels. Follow @research_nest for daily art made by computer programs and AI.
			   \n#trn #dailyposts #deeplearning #ai #art #aiart'''

topics = ['nature',
          'animals',
          'flowers',
          'architecture',
          'background',
          'scenery',
          'wallpaper',
          'outdoors',
          'sunset']

news_topics = ['science', 'technology', 'deep learning', 'research', 'blockchain']

style = ['style_1.jpg',
         'style_3.jpg',
         'style_4.jpg',
         'style_6.jpg',
         'style_8.jpg',
         'style_9.jpg']

twitterEngine = TwitterEngine(
    TWITTER_CONSUMER_KEY=TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET=TWITTER_CONSUMER_SECRET,
    TWITTER_ACCESS_TOKEN=TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET=TWITTER_ACCESS_TOKEN_SECRET)

artEngine = ArtEngine(TRN_PEXELS_API_KEY=TRN_PEXELS_API_KEY)

newEngine = NewsEngine(NEWS_API_KEY=NEWS_API_KEY)

# %%
starttime = time.time()
count = 0
while True:
    count = count + 1
    print('count', count)
    if count % 5 == 0:
        news_topic = random.choice(news_topics)
        data = newEngine.fetchNews(news_topic, 1)
        tweet = generateNewsTweet(data, news_topic)
        if tweet != None:
            twitterEngine.doTweet(tweet)
            print('News Tweeted!')
    else:
        img = artEngine.curateArt(random.choice(topics), random.choice(style))
        twitterEngine.doTweetWithMedia(tweet_art, img)
        print('Artwork Tweeted!')

    time.sleep(1800.0 - ((time.time() - starttime) % 1800.0))
