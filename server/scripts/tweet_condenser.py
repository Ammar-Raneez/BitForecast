import pandas as pd
from tqdm import tqdm

OUTPUT_PATH = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/Tweets/BTC_Tweet_Sentiment_Unweighed.csv'

def dt(x):
    '''
    helper function to create pandas date
    '''

    t = pd.Timestamp(x)
    return pd.Timestamp.date(t)

def read_csv():
    '''
    Load all existing condensed csv
    '''

    df = pd.read_csv(f'{OUTPUT_PATH}', engine='python')
    return df

def condense(dfs):
    '''
    Condense tweet dfs into a single df of averaged sentiment values for each date
    '''

    condensed_df = None
    existing_df = read_csv()

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

    condensed_combined_df = pd.concat([existing_df, condensed_df])
    condensed_combined_df.date = condensed_combined_df.date.apply(dt)
    condensed_combined_df.sort_values(['date'], inplace=True)

    # Remove duplicate dates
    condensed_combined_df = condensed_combined_df[~condensed_combined_df.date.duplicated(keep='first')]

    # Filter only required columns
    condensed_combined_df_required = condensed_combined_df[['date', 'negative_score', 'neutral_score', 'positive_score', 'compound_score']]
    return condensed_combined_df_required

def export_data(df):
    '''
    Save data
    '''

    df.to_csv(OUTPUT_PATH)

def condense_tweets(dfs):
    '''
    Main runner
    dfs -> comes from the sentiment_analysis script (only the new fetched dates)
    '''

    print('\nRunning tweet condensation...', end='\n')
    condensed_df = condense(dfs)
    export_data(condensed_df)
    print('\nTweet condensation performed', end='\n')
