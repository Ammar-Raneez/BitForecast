from pytrends.request import TrendReq
import pandas as pd
import numpy as np

FILE_PATH = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/GTrends/BTC_GTrends_total_cleaned.csv'

def get_available_data():
    '''
    Get current available data
    '''

    df = pd.read_csv(FILE_PATH)

    # Ensure date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])
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
    combined_df.index = pd.to_datetime(combined_df.index)
    combined_df = combined_df[~combined_df.index.duplicated(keep='first')]

    # Round value
    combined_df['bitcoin_unscaled'] = [int(np.ceil(i)) for i in combined_df['bitcoin_unscaled']]
    combined_df.sort_index(inplace=True)
    return combined_df

def export_data(df):
    '''
    Save data
    '''

    df.to_csv(FILE_PATH)

def update_trends():
    '''
    Main runner
    '''

    print('\nRunning google trends scraper...', end='\n')
    df = update_data()
    export_data(df)
    print('\nGoogle trends data updated', end='\n')

    # Return for script
    return df

if __name__ == '__main__':
    update_trends()
