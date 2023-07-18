# gpt4twitter
Simple script for a macroeconomics AI Twitter bot powered by Federal Reserve Data and OpenAI's GPT-4

Here's the [YouTube Video]().

## Installation

```
pip install pandas_datareader sklearn schedule tweepy pytz
```

Set your API keys via environment variables, eg. [OpenAI API key](https://platform.openai.com/account/api-keys) and [Twitter API access](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api). 

export FRED_API_KEY=YOUR_KEY
export OPENAI_API_KEY=YOUR_KEY
export TACCESS_KEY=YOUR_KEY
export CONSUMER_KEY=YOUR_KEY
export CONSUMER_SECRET_KEY=YOUR_KEY
export TACCESSTOKEN_KEY=YOUR_KEY

## Example usage
```
> python src/main.py
```
