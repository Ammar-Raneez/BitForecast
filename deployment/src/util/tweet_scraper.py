import snscrape.modules.twitter as sntwitter
import pandas as pd
from lingua import Language, LanguageDetectorBuilder

import datetime
from tqdm import tqdm

from src.util.sentiment_analysis import analyze_sentiments
from src.util.tweet_condenser import condense_tweets
from src.util.mongodb import init_mongodb, TWITTER_SENTIMENTS_COLLECTION

detector = LanguageDetectorBuilder.from_languages(Language.ENGLISH, Language.GERMAN).build()

def dt(x):
    '''
    helper function to create pandas date
    '''

    t = pd.Timestamp(x)
    return pd.Timestamp.date(t)

def read_mongo_dates():
    '''
    Read existing sentiments' dates from MongoDB
    '''

    db = init_mongodb()
    sentiments = db[TWITTER_SENTIMENTS_COLLECTION].find_one()

    # first value is the document id 
    del sentiments['_id']

    # Extract date fields
    return [sentiment['date'] for sentiment in sentiments.values()]

def get_dates():
    '''
    Get list of dates that must be scraped
    '''

    today =  datetime.datetime.today().strftime('%Y-%m-%d')
    latest_date = max(read_mongo_dates())

    # From dates after including date (don't refetch latest date)
    from_date = pd.Timestamp(latest_date) + datetime.timedelta(days=1)

    # Include fetching today's data
    till_date = pd.Timestamp(today) + datetime.timedelta(days=1)

    dates = pd.date_range(
        from_date.date(),
        till_date.date()-datetime.timedelta(days=1),freq='d'
    )

    return today, latest_date, dates

def scrape_tweets(dates):
    '''
    Scrape tweets of the specified dates
    '''

    tweets_list = {}
    for i, date in tqdm(enumerate(dates)):
        print(f'Trying date: {date} | Currently at index: {i}')
        try:
            next_day = pd.Timestamp(date) + datetime.timedelta(days=1)
            for j, tweet in tqdm(enumerate(sntwitter.TwitterSearchScraper(
                f'#bitcoin -filter:retweets since:{dt(date).strftime("%Y-%m-%d")} until:{dt(next_day).strftime("%Y-%m-%d")}'
            ).get_items())):
                if j > 500:
                    break
                if not tweets_list.get(date):
                    tweets_list[date] = []
                tweets_list[date].append([tweet.date, tweet.user, tweet.retweetCount, tweet.likeCount, tweet.rawContent])
        except Exception as e:
            print(f'Error: {e}')

    return tweets_list

def process_tweets(tweets_list):
    '''
    Create dataframe from the tweets dictionary
    '''

    dates = []
    usernames = []
    user_total_followers = []
    user_total_listed = []
    tweet_retweets = []
    tweet_likes = []
    texts = []

    for i, val in enumerate(tweets_list.values()):
        for j in val:
            dates.append(j[0])
            usernames.append(j[1].username)
            user_total_followers.append(j[1].followersCount)
            user_total_listed.append(j[1].listedCount)
            tweet_retweets.append(j[2])
            tweet_likes.append(j[3])
            texts.append(j[-1])

    df_details = {
        'user': usernames,
        'timestamp': dates,
        'user_total_followers': user_total_followers,
        'user_total_listed': user_total_listed,
        'tweet_retweets': tweet_retweets,
        'tweet_likes': tweet_likes,
        'text': texts
    }

    df = pd.DataFrame(df_details)
    df.timestamp = df.timestamp.apply(dt)
    scraped_dfs = [y for x, y in df.groupby('timestamp')]
    return scraped_dfs

def clean_tweets(dates):
    '''
    Clean tweets that have empty records and non-english tweets
    '''

    print('Scraping tweets...\n')
    tweets_list = scrape_tweets(dates)
    print('Tweets scraped\n')
    scraped_dfs = process_tweets(tweets_list)

    print('Cleaning tweets...\n')
    for i, df in enumerate(tqdm(scraped_dfs)):
        if df.iloc[0].get('timestamp'):
            filename = str(df.iloc[0]['timestamp'])
        else:
            filename = str(df.iloc[0]['date'])

        print(f'Currently at df: {i+1} | {filename}')
        df.dropna(subset=['user', 'timestamp', 'text', 'user_total_followers', 'user_total_listed', 'tweet_retweets', 'tweet_likes'], inplace=True)
        L = []
        for row in df['text']:
            # Use lingua to remove any non-english observations
            if len(row) != 0:
                L.append(detector.detect_language_of(row))
            else:
                L.append(None)

        df['lang'] = L
        df_filtered = df.loc[df.loc[:, 'lang'] == Language.ENGLISH].copy(deep=True)
        df_filtered.drop(['lang'], axis=1, inplace=True)

    print('Tweets cleaned\n')
    return scraped_dfs

def update_tweets():
    '''
    Main runner
    '''

    print('Running tweet scraper...\n')
    today, latest_date, dates = get_dates()
    print(dates)
    print()
    scraped_dfs = clean_tweets(dates)
    sentiment_analyzed_dfs = analyze_sentiments(scraped_dfs)
    condensed_tweets = condense_tweets(sentiment_analyzed_dfs)
    print('Tweet data and sentiments updated\n')

    # Return for scripts
    return condensed_tweets
