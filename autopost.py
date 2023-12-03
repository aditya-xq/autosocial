# autopost.py

import logging
from twitter import post_tweet
from logging_config import setup_logging

def main():
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # Example of posting a tweet
    tweet_text = "Hello, this is tweet number 2!"
    post_tweet(tweet_text)

# Run the main function
if __name__ == "__main__":
    main()
