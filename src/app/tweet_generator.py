import tweepy
import os, requests, json, logging
from utils.utils import truncate_sentences

# API Credentials
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET_KEY")
access_token = os.getenv("TACCESS_KEY")
access_token_secret = os.getenv("TACCESSTOKEN_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

def generate_tweet(conversation):
    # OpenAI call
    model_str = "gpt-4"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(openai_key),
    }
    dataload = {
        "model": model_str,
        "messages": conversation,  # we now send in the conversation list, not just the prompt string
        "temperature": 0.6,
    }
    response = requests.post(url, headers=headers, data=json.dumps(dataload)) 
    answer = response.json()['choices'][0]['message']['content']
    print('OpenAI generated tweet: ', answer)
    tokenusage = response.json()['usage']
    logging.info(f'Token usage: {tokenusage}.')
    print(f'Token usage: {tokenusage}.')
    
    return answer, tokenusage

def send_tweet(answer):
    # Authenticate with the Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    # sends the tweet and prints link to tweet
    response = client.create_tweet(text=truncate_sentences(answer))
    
    print(f"https://twitter.com/user/status/{response.data['id']}")

    return response
