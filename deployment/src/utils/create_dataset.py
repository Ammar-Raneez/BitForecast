import pandas as pd

from utils.mongodb import init_mongodb

def get_prices(historical_prices):
    '''
    Load and clean historical prices dataset
    '''

    # Safe check to remove a column that comes sometimes
    try:
        historical_prices.drop(['Unnamed: 0'], axis=1, inplace=True)
    except:
        pass

    historical_prices.drop(['max', 'min', 'open'], axis=1, inplace=True)
    filtered_prices = historical_prices.loc[~(historical_prices.loc[:, 'date'] < '2015-01-01')].copy(deep=True)
    return filtered_prices

def get_twitter_volume(twitter_volume):
    '''
    Load and clean twitter volume dataset
    '''

    # Safe check to remove a column that comes sometimes
    try:
        twitter_volume.drop(['Unnamed: 0'], axis=1, inplace=True)
    except:
        pass

    filtered_t_volume = twitter_volume.loc[~(twitter_volume.loc[:, 'Date'] < '2015-01-01')].copy(deep=True)
    return filtered_t_volume

def get_block_reward(block_reward):
    '''
    Load and clean block reward dataset
    '''

    # Safe check to remove a column that comes sometimes
    try:
        block_reward.drop(['Unnamed: 0'], axis=1, inplace=True)
    except:
        pass

    filtered_block_reward = block_reward.loc[~(block_reward.loc[:, 'Date'] < '2015-01-01')].copy(deep=True)
    return filtered_block_reward

def get_google_trends(gtrends):
    '''
    Load and clean google trends dataset
    '''

    # Safe check to remove a column that comes sometimes
    try:
        gtrends.drop(['Unnamed: 0'], axis=1, inplace=True)
    except:
        pass

    filtered_gtrends = gtrends.loc[~(gtrends.loc[:, 'Date'] < '2015-01-01')].copy(deep=True)
    return filtered_gtrends

def get_twitter_sentiment(twitter_sentiments):
    '''
    Load and clean twitter sentiment dataset
    '''

    # Safe check to remove a column that comes sometimes
    try:
        twitter_sentiments.drop(['Unnamed: 0'], axis=1, inplace=True)
    except:
        pass

    twitter_sentiments.drop(['negative_score', 'neutral_score', 'positive_score'], axis=1, inplace=True)
    filtered_twitter_sentiments = twitter_sentiments.loc[~(twitter_sentiments.loc[:, 'date'] < '2015-01-01')].copy(deep=True)
    return filtered_twitter_sentiments

def get_exogenous_datasets(
    block_reward,
    trends,
    tweet_volume,
    tweets
):
    '''
    Load in, clean and format all the datasets to use
    '''

    filtered_block_reward = get_block_reward(block_reward)
    filtered_gtrends = get_google_trends(trends)
    filtered_twitter_volume = get_twitter_volume(tweet_volume)
    # filtered_twitter_sentiments = get_twitter_sentiment(tweets)

    exogenous_features = [
        filtered_block_reward,
        filtered_gtrends,
        filtered_twitter_volume,
        # filtered_twitter_sentiments
    ]

    for i in exogenous_features:
        i.rename(columns={ 'Date': 'date' }, inplace=True)

    for i in exogenous_features:
        i.loc[:, 'date'] = (pd.to_datetime(i.loc[:, 'date'])).dt.strftime('%Y-%m-%d')

    return exogenous_features

def create_combined_dataset(
    prices,
    block_reward,
    trends,
    tweet_volume,
    tweets
):
    '''
    Create and clean the final combined dataset
    '''

    exogenous_features = get_exogenous_datasets(
        block_reward,
        trends,
        tweet_volume,
        tweets
    )

    filtered_prices = get_prices(prices)

    combined_df = filtered_prices.copy(deep=True)

    # Combine datasets together and add NaN to empty date rows
    for i in exogenous_features:
        combined_df = pd.merge(
            combined_df,
            i,
            on=['date'],
            how='left'
        )

    # Impute missing values with the respective columns mean
    combined_df.fillna(combined_df.mean(numeric_only=True), inplace=True)
    combined_df['date'] = pd.to_datetime(combined_df['date'])
    return combined_df

def export_data(df):
    '''
    Save data
    '''

    # Store datasets in mongodb for any requirements in production
    df.index = df.index.astype(str)
    df_dict = df.to_dict('index')
    dataset_db = init_mongodb()
    dataset_db['Final Dataset'].delete_many({})
    dataset_db['Final Dataset'].insert_one(df_dict)

def create_final_dataset(
    prices,
    block_reward,
    trends,
    tweet_volume,
    tweets
):
    '''
    Main runner
    '''

    print('\nRunning final dataset creation...', end='\n')
    combined_df = create_combined_dataset(
        prices,
        block_reward,
        trends,
        tweet_volume,
        tweets
    )

    export_data(combined_df)
    print('\nFinal dataset created', end='\n')
