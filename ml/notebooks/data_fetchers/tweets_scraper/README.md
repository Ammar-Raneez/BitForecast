Contains code that was used to initially fetch all the tweet data, before it was converted into a script under server

<em>Two old datasets were used instead of fetching all historical tweets</em>
* [dataset 01](https://www.kaggle.com/datasets/alaix14/bitcoin-tweets-20160101-to-20190329)
* [dataset 02](https://www.kaggle.com/datasets/kaushiksuresh147/bitcoin-tweets)

Files:
* `bitcoin_tweets_filteration_large.ipynb` - breaks down dataset 01 into daily files
* `bitcoin_tweets_filteration_small.ipynb` - breaks down dataset 02 into daily files
* `tweet_fetcher.ipynb` - attempts techniques to fetch the remaining tweets that are not in the two datasets
* `tweet_scraper.ipynb` - fetches tweets ahead in time of the datasets, and any missing dates of the datasets
