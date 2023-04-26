'''
This file will perform sentiment analysis on the obtained dataframes via
the VADER sentiment library
'''

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import math
from tqdm import tqdm

def preprocess(text):
    '''
    Required preprocessing for VADER
    Remove username and link placeholders
    (not required to perform other steps because of the heuristics of VADER)
    '''

    new_text = []
    for t in text.split(' '):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return ' '.join(new_text)

def calculate_sentiment(sentence):
    '''
    Calculate the sentiment of a single tweet (sentence)
    '''

    sid_obj = SentimentIntensityAnalyzer()
    try:
        sentiment_dict = sid_obj.polarity_scores(sentence)        
        return sentiment_dict['neg'], sentiment_dict['neu'], sentiment_dict['pos'], sentiment_dict['compound']
    except Exception as e:
        print(f'Something went wrong with this sentence: {sentence}')
        return e

def analyze_sentiment(dfs):
    '''
    Updates all dfs with respective sentiment columns
    '''

    sentiment_analyzed_dfs = []
    for i, df in tqdm(enumerate(dfs)):
        # Certain files have timestamp, certain have date
        if df.iloc[0].get('timestamp'):
            df_filename = str(df.iloc[0]['timestamp'])
        else:
            df_filename = str(df.iloc[0]['date'])

        print(f'Currently at df: {i+1} | {df_filename}')
        negative_scores = []
        positive_scores = []
        neutral_scores = []
        compound_scores = []

        for j in range(df.shape[0]):
            try:
                neg, neu, pos, compound = calculate_sentiment(preprocess(df.iloc[j]['text']))
            except:
                neg, neu, pos, compound = None, None, None, None

            negative_scores.append(neg)
            positive_scores.append(pos)
            neutral_scores.append(neu)

            # Weigh the compound score here based on the proposed formula
            weighted_compound_score = compound
            alpha, beta, gamma, delta = 0.5, 0.3, 0.1, 0.1
            followers, lists, retweets, likes = df.iloc[j]['user_total_followers'], df.iloc[j]['user_total_listed'], df.iloc[j]['tweet_retweets'], df.iloc[j]['tweet_likes']
            weighted_followers = alpha * math.log10(followers + 1)
            weighted_lists = beta * math.log10(lists + 1)
            weighted_retweets = gamma * math.log10(retweets + 1)
            weighted_likes = delta * math.log10(likes + 1)
            weighted_sum = weighted_followers + weighted_lists + weighted_retweets + weighted_likes
            influencer_score = weighted_sum / (weighted_sum + 1)
            weighted_compound_score *= influencer_score
            compound_scores.append(weighted_compound_score)

        df['negative_score'] = negative_scores
        df['positive_score'] = positive_scores
        df['neutral_score'] = neutral_scores
        df['compound_score'] = compound_scores
        sentiment_analyzed_dfs.append(df)

    return sentiment_analyzed_dfs

def analyze_sentiments(dfs):
    '''
    Main runner
    dfs -> comes from the tweet_scraper script (only the new fetched dates)
    '''

    print('Running sentiment analysis...\n')
    sentiment_analyzed_dfs = analyze_sentiment(dfs)
    print('Tweet sentiment analysis performed\n')
    return sentiment_analyzed_dfs
