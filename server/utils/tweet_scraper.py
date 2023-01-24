import snscrape.modules.twitter as sntwitter
import pandas as pd
from lingua import Language, LanguageDetectorBuilder

import datetime
import os
from tqdm import tqdm

# Hack to import modules from another directory
import sys
sys.path.append( '.' )

from server.scripts.sentiment_analysis import analyze_sentiments
from server.scripts.tweet_condenser import condense_tweets

FOLDER_PATH = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/Tweets/tweets_complete'
detector = LanguageDetectorBuilder.from_languages(Language.ENGLISH, Language.GERMAN).build()

def dt(x):
    '''
    helper function to create pandas date
    '''

    t = pd.Timestamp(x)
    return pd.Timestamp.date(t)

def get_dates():
    '''
    Get list of dates that must be scraped
    '''

    today =  datetime.datetime.today().strftime('%Y-%m-%d')
    latest_date = max([i.replace('.csv', '') for i in os.listdir(FOLDER_PATH)[:-1]])

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
                tweets_list[date].append([tweet.date, tweet.user.username, tweet.rawContent])
        except Exception as e:
            print(f'Error: {e}')

    return tweets_list

def process_tweets(tweets_list):
    '''
    Create dataframe from the tweets dictionary
    '''

    dates = []
    usernames = []
    texts = []

    for i, val in enumerate(tweets_list.values()):
        for j in val:
            dates.append(j[0])
            usernames.append(j[1])
            texts.append(j[2])

    df_details = {
        'user': usernames,
        'timestamp': dates,
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

    tweets_list = scrape_tweets(dates)
    scraped_dfs = process_tweets(tweets_list)

    for df in scraped_dfs:
        df.dropna(subset=['user', 'timestamp', 'text'], inplace=True)

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
        filename = str(df.iloc[0]['timestamp'])
        df_filtered.to_csv(f'{FOLDER_PATH}/{filename}.csv')

    return scraped_dfs

def update_tweets():
    '''
    Main runner
    '''

    print('\nRunning tweet scraper...', end='\n')
    today, latest_date, dates = get_dates()
    scraped_dfs = clean_tweets(dates)
    sentiment_analyzed_dfs = analyze_sentiments(scraped_dfs)
    condense_tweets(sentiment_analyzed_dfs)
    print('\nTweet data and sentiments updated', end='\n')

if __name__ == '__main__':
    '''
    Scrape tweets, analyze sentiments and condense tweets
    '''

    update_tweets()
