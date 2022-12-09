import snscrape.modules.twitter as sntwitter
import pandas as pd
from whatthelang import WhatTheLang

import datetime
import os
from tqdm import tqdm

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
    latest_date = max([i.replace('.csv', '') for i in os.listdir('../../../data/tweets/tweets_complete')[:-1]])

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

                tweets_list[date].append([tweet.date, tweet.username, tweet.content])
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
        'user_name': usernames,
        'date': dates,
        'text': texts
    }

    df = pd.DataFrame(df_details)
    df.date = df.date.apply(dt)
    df_days = [y for x, y in df.groupby('date')]
    return df_days

def clean_tweets(dates):
    '''
    Clean tweets that have empty records and non-english tweets
    '''

    wtl = WhatTheLang()
    tweets_list = scrape_tweets(dates)
    df_days = process_tweets(tweets_list)

    for df in df_days:
        df.dropna(subset=['user_name', 'date', 'text'], inplace=True)

        L = []
        for row in df['text']:
            # Use WTL to remove any non-english observations
            if len(row) != 0:
                L.append(wtl.predict_lang(row))
            else:
                L.append(None)

        df['lang'] = L
        df_filtered = df[df['lang'] == 'en']
        df_filtered.drop(['lang'], axis=1, inplace=True)
        filename = str(df.iloc[0]['date'])
        df_filtered.to_csv(f'../../ml/data/Tweets/tweets_complete/{filename}.csv')

    return df_days

def update_tweets():
    '''
    Main runner
    '''

    today, latest_date, dates = get_dates()
    df_days = clean_tweets(dates)
    return df_days
