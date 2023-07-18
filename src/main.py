from data.fetcher import fetch_data
from app.tweet_generator import generate_tweet, send_tweet
from utils.conversation_manager import load_conversation, append_conversation

import datetime, pytz, random, time, os

# API Credentials
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET_KEY")
access_token = os.getenv("TACCESS_KEY")
access_token_secret = os.getenv("TACCESSTOKEN_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

def job():
    try:
        frednat, new_data = fetch_data()
        past_tweets, conversation, user_prompts = load_conversation(new_data, frednat)
        answer, tokenusage = generate_tweet(conversation)
        response = send_tweet(answer)
        append_conversation(past_tweets, answer, conversation[-1]['content'])
        print('Wrote tweet history')
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)

def run_at_time():
    time_now = datetime.datetime.now(pytz.timezone('US/Eastern'))
    hour_to_run = random.randint(9, 11)
    minute_to_run = random.randint(0, 59)

    if time_now.hour < hour_to_run or (time_now.hour == hour_to_run and time_now.minute < minute_to_run):
        next_run_time = time_now.replace(hour=hour_to_run, minute=minute_to_run)
    else:
        next_run_time = (time_now + datetime.timedelta(days=1)).replace(hour=hour_to_run, minute=minute_to_run)

    seconds_until_next_run = (next_run_time - time_now).total_seconds()
    print(f"Scheduled to run at {next_run_time} Eastern Standard Time")
    time.sleep(seconds_until_next_run)
    job()    

while True:
    run_at_time()
    time.sleep(600)
