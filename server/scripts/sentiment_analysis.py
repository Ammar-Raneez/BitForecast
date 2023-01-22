from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from tqdm import tqdm

FOLDER_PATH = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/Tweets'

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
            compound_scores.append(compound)

        df['negative_score'] = negative_scores
        df['positive_score'] = positive_scores
        df['neutral_score'] = neutral_scores
        df['compound_score'] = compound_scores
        sentiment_analyzed_dfs.append(df)
        export_data(df, df_filename)

    return sentiment_analyzed_dfs

def export_data(df, filename):
    '''
    Save data
    '''

    df.to_csv(f'{FOLDER_PATH}/{filename}.csv')

def analyze_sentiments(dfs):
    '''
    Main runner
    dfs -> comes from the tweet_scraper script (only the new fetched dates)
    '''

    print('\nRunning sentiment analysis...', end='\n')
    sentiment_analyzed_dfs = analyze_sentiment(dfs)
    return sentiment_analyzed_dfs
