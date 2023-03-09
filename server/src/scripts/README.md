Contains necessary scripts required to either process the scraped data or
to create the dataset

* `create_dataset.py` - creates the combined dataset from the scraped data
* `sentiment_analysis.py` - performs sentiment analysis on the scraped tweet data
* `tweet_condenser.py` - condenses the scraped tweet data of multiple date CSVs into a single file
* `update_data.py` - main script that utilizes the scrapers and other scripts to create the combined final dataset to be used by the model
