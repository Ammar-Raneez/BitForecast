import pandas as pd
import os
from tqdm import tqdm

FOLDER_PATH = '../../ml/data/Tweets/tweets_complete_sentiment_unweighed'
OUTPUT_PATH = '../../ml/data/Tweets/BTC_Tweet_Sentiment_Unweighed.csv'
ALL_FILES = os.listdir(FOLDER_PATH)

def read_csvs():
    '''
    Load all tweet csvs in folder into a list of dfs which can then be condensed
    '''

    dfs = [pd.read_csv(f'{FOLDER_PATH}/{i}', engine='python') for i in ALL_FILES]
    return dfs

def condense_tweets(dfs):
    '''
    Condense tweet dfs into a single df of averaged sentiment values
    for each date
    '''

    condensed_df = None

    for i, df in tqdm(enumerate(dfs)):
        # Certain files have timestamp column, certain have date
        if df.iloc[0].get('timestamp'):
            df_filename = str(df.iloc[0]['timestamp'])
        else:
            df_filename = str(df.iloc[0]['date'])
        print(f'Currently at df: {i+1} | {df_filename}')

        # Get the average values for each date
        averages = list(df[['negative_score', 'neutral_score', 'positive_score', 'compound_score']].mean())
        data = {
            'date': [df_filename],
            'negative_score': averages[0],
            'neutral_score': averages[1],
            'positive_score': averages[2],
            'compound_score': averages[3],
        }

        tweet_df = pd.DataFrame(data, index=None)
        if condensed_df is not None:
            condensed_df = pd.concat([condensed_df, tweet_df])
        else:
            condensed_df = pd.DataFrame(data, index=None)

    return condensed_df

def export_data(df):
    '''
    Save data
    '''

    df.to_csv(OUTPUT_PATH)
