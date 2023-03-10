import pandas as pd

TRENDS_DATA = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/GTrends/BTC_GTrends_total_cleaned.csv'
TWEETS_DATA = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/Tweets/BTC_Tweet_Sentiment_Unweighed.csv'
TWEET_VOLUME_DATA = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/Tweets/BTC_Tweet_Volume.csv'
BLOCK_REWARD_DATA = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/BTC_Block_Reward.csv'
BTC_PRICES_DATA = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/BTC_Prices.csv'

OUTPUT_PATH = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/combined_data.csv'

def get_prices(historical_prices = None):
    '''
    Load and clean historical prices dataset
    '''

    if not historical_prices:
        historical_prices = pd.read_csv(BTC_PRICES_DATA)

    historical_prices.drop(['max', 'min', 'open'], axis=1, inplace=True)
    filtered_prices = historical_prices.loc[~(historical_prices.loc[:, 'date'] < '2015-01-01')].copy(deep=True)
    return filtered_prices

def get_twitter_volume(twitter_volume = None):
    '''
    Load and clean twitter volume dataset
    '''

    if not twitter_volume:
        twitter_volume = pd.read_csv(TWEET_VOLUME_DATA)

    twitter_volume.drop(['Unnamed: 0'], axis=1, inplace=True)
    filtered_t_volume = twitter_volume.loc[~(twitter_volume.loc[:, 'Date'] < '2015-01-01')].copy(deep=True)
    return filtered_t_volume

def get_block_reward(block_reward = None):
    '''
    Load and clean block reward dataset
    '''

    if not block_reward:
        block_reward = pd.read_csv(BLOCK_REWARD_DATA)

    block_reward.drop(['Unnamed: 0'], axis=1, inplace=True)
    filtered_block_reward = block_reward.loc[~(block_reward.loc[:, 'Date'] < '2015-01-01')].copy(deep=True)
    return filtered_block_reward

def get_google_trends(gtrends = None):
    '''
    Load and clean google trends dataset
    '''

    if not gtrends:
        gtrends = pd.read_csv(TRENDS_DATA)

    filtered_gtrends = gtrends.loc[~(gtrends.loc[:, 'date'] < '2015-01-01')].copy(deep=True)
    return filtered_gtrends

def get_twitter_sentiment(twitter_sentiments = None):
    '''
    Load and clean twitter sentiment dataset
    '''

    if not twitter_sentiments:
        twitter_sentiments = pd.read_csv(TWEETS_DATA)

    twitter_sentiments.drop(['Unnamed: 0', 'negative_score', 'neutral_score', 'positive_score'], axis=1, inplace=True)
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
    filtered_twitter_sentiments = get_twitter_sentiment(tweets)

    exogenous_features = [
        filtered_block_reward,
        filtered_gtrends,
        filtered_twitter_volume,
        filtered_twitter_sentiments
    ]

    for i in exogenous_features:
        i.rename(columns={ 'Date': 'date' }, inplace=True)

    for i in exogenous_features:
        i.loc[:, 'date'] = (pd.to_datetime(i.loc[:, 'date'])).dt.strftime('%Y-%m-%d')

    return exogenous_features

def create_combined_dataset(
    prices = None,
    block_reward = None,
    trends = None,
    tweet_volume = None,
    tweets = None
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
    return combined_df

def export_data(df):
    '''
    Save data
    '''

    df.to_csv(OUTPUT_PATH)

def create_final_dataset(
    prices = None,
    block_reward = None,
    trends = None,
    tweet_volume = None,
    tweets = None
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

if __name__ == '__main__':
    create_final_dataset()
