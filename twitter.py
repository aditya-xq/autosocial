import os
from requests_oauthlib import OAuth1Session
import logging
from dotenv import load_dotenv

from logging_config import setup_logging

# Load environment variables
load_dotenv()

# Set up logging as per the provided configuration
setup_logging()
logger = logging.getLogger(__name__)

def post_tweet(text):
    """
    Post a tweet with the given text.

    Args:
    text (str): The text of the tweet to be posted.

    Returns:
    bool: True if the tweet was posted successfully, False otherwise.
    """
    try:
        # Retrieve variables from .env file
        api_key = os.getenv("API_KEY")
        api_secret_key = os.getenv("API_KEY_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

        # OAuth 1 Session
        twitter = OAuth1Session(api_key, client_secret=api_secret_key, 
                                resource_owner_key=access_token, 
                                resource_owner_secret=access_token_secret)

        # URL for the request
        url = "https://api.twitter.com/2/tweets"

        # Data to be sent
        payload = {"text": text}

        # Make the POST request
        response = twitter.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 201:
            logger.info(f"Tweet posted successfully: {text}")
            return True
        else:
            logger.error(f"Failed to post tweet: {response.text}")
            return False

    except Exception as e:
        logger.exception(f"Error while trying to post tweet: {e}")
        return False
