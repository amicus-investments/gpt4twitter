import os, json
from collections import deque

def load_conversation(new_data, frednat):
    # Load in old tweets and user prompts
    lookback = 21 # days to store in deque
    past_tweets = deque(maxlen=lookback)
    conversation = [{"role": "system", "content": "Generate tweets as if you were an expert economist. The tweet should not exceed 280 characters including spaces. Do not add any tags and make sure to only use natural language. Do not repeat the content from previous tweets. Do not repeat the data points mentioned in the previous tweets. Stay within the single tweet length. Do not use confusing abbreviations a lay audience would not understand, but make sure to mention this is United States official government data and cite values where appropriate."}]  # stores the conversation history

    if os.path.exists('data/prev.txt'):
        with open('data/prev.txt', 'r') as f:
            lines = f.readlines()

        lines = lines[-lookback:]

        for i, line in enumerate(lines):
            role = 'assistant' if i % 2 == 1 else 'user'
            content = line.rstrip('\n')
            past_tweets.append(content)
            conversation.append({'role': role, 'content': content})

    prevs = '. '.join(past_tweets)

    if os.path.exists('data/user_prompts.txt'):
        with open('data/user_prompts.txt', 'r') as f:
            user_prompts = [line.rstrip('\n') for line in f]

    # Done loading conversation. Now reminder or generate tweet
    if new_data:
        pschema = f'Generate a tweet on the FRED macroeconomic data as if you were an expert economist. The tweet should not exceed 280 characters including spaces. Do not add any tags and make sure to only use natural language. Do not repeat the content from previous tweets. Do not repeat the data points mentioned in the previous tweets. Stay within the single tweet length. Do not use confusing abbreviations a lay audience would not understand, but make sure to mention this is from official government data and cite values where appropriate: Previous tweets: {prevs}. FRED data: {frednat} Do not repeat the data points mentioned in the previous tweets.'
    elif (2*len(past_tweets)+1) % 3 == 0: # reminder time
        pschema = "Remember don't overuse abbreviations and reuse figures. You already repeated those figures in your previous tweets which were also too long. Generate a short unique tweet."
    else:
        pschema = 'Generate another tweet.'
    
    conversation.append({'role': 'user', 'content': pschema})

    return past_tweets, conversation, user_prompts

def append_conversation(past_tweets, answer, pschema):
    # push tweet onto deque and backup
    past_tweets.append(answer)

    # append to keep all history
    with open('data/prev.txt', 'a') as f:
        f.write(answer + '\n')

    # Append user prompt
    with open('data/user_prompts.txt', 'a') as f:
        f.write(pschema+'\n')
