from pytrends.request import TrendReq
import pandas as pd
import numpy as np

def get_available_data():
    '''
    Get current available data
    '''

    df = pd.read_csv('../../ml/data/GTrends/BTC_GTrends_total_cleaned.csv')
    df.sort_values(['date'], inplace=True)
    return df

def get_new_trends_data():
    '''
    Fetch latest Trends data
    '''

    pytrends = TrendReq()
    kw_list = ['bitcoin']
    pytrends.build_payload(
        kw_list,
        cat=0,
        timeframe='now 7-d',
        geo='',
        gprop=''
    )

    curr_data = pytrends.interest_over_time()
    return curr_data

def format_new_data(df):
    '''
    Converts the obtained data into the format of the available data
    '''

    df.rename(columns={ 'bitcoin': 'bitcoin_unscaled' }, inplace=True)

    # Create stringified dates
    df.index = [str(i) for i in pd.to_datetime(df.index).date]
    df.index.rename('date', inplace=True)

    # As the data obtained is for every hour, get an average of it all for each day
    grouped_df = df.groupby(level=0)
    avg_df = grouped_df.agg({ 'bitcoin_unscaled': 'mean' })
    return avg_df

def clean_new_data():
    '''
    Remove unneeded columns of fetched data
    '''

    df = get_new_trends_data()
    df.drop(['isPartial'], axis=1, inplace=True)
    avg_df = format_new_data(df)
    return avg_df

def update_data():
    '''
    Main runner. Combines existing data & new data as to create
    an updated dataframe
    '''

    avail_df = get_available_data()
    curr_df = clean_new_data()

    avail_df.set_index('date', inplace=True)
    combined_df = pd.concat([avail_df, curr_df])

    # Remove any duplicate observations
    combined_df = combined_df[~combined_df.index.duplicated(keep='first')]

    # Round value
    combined_df['bitcoin_unscaled'] = [int(np.ceil(i)) for i in combined_df['bitcoin_unscaled']]
    return combined_df

def export_data(df):
    '''
    Save data
    '''

    df.to_csv('../../ml/data/GTrends/BTC_GTrends_total_cleaned.csv')
