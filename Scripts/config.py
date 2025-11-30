import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Play Store App IDs
APP_IDS={
    'CBE' : os.getenv('CBE_APP_ID', 'com.combanketh.mobilebanking'),
    'Awash' : os.getenv('AWASH_APP_ID', 'com.sc.awashpay'),
    'Dashen' : os.getenv('DASHEN_APP_ID', 'com.dashen.dashensuperapp'),
}

# Bank Names Mapping
BANK_NAMES={
    'CBE' : 'Commercial Bank of Ethiopia',
    'Awash' : 'Awash Bank',
    'Dashen' : 'Dashen Bank',
}

# Scraping Configuration
SCRAPING_CONFIG={
    'rewiews_per_bank' : int(os.getenv('REVIEWS_PER_BANK',400)),
    'max-retries': int(os.getenv('MAX_RETRIES',3)),
    'lang': 'en',
    'country': 'et'
}

# file paths
DATA_PATHS={
    'raw':'data/raw',
    'processed':'data/processed',
    'raw_reviews':'data/raw/reviews_raw.csv',
    'processesd_reviews':'data/processed/reviews_processed.csv',
    'sentiment_results':'data/processed/reviews_with_sentiments.csv',
    'final_results':'data/processed/reviews_final.csv'
}
