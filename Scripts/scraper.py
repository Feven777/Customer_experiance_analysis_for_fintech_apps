import sys
import os

# Add parent directory to path to allow importing modules from there
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google_play_scraper import app,Sort,reviews_all,reviews
import pandas as pd
from datetime import datetime 
import time
from tqdm import tqdm
from config  import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS


class PlayStoreScraper:

    def __init__(self):
        self.app_ids=APP_IDS,
        self.bank_names = BANK_NAMES,
        self.reviews_per_bank= SCRAPING_CONFIG['reviews_per_bank'],
        self.lang =SCRAPING_CONFIG['lang'],
        self.country=SCRAPING_CONFIG['country'],
        self.max_retries=SCRAPING_CONFIG['max_retries']
    
    def get_app_info(self, app_id):

        try:
            result=app(app_id,lang=self.lang,country=self.country)
            return{
                'app_id': app_id,
                'title': result.get('title','N/A'),
                'score': result.get('score',0),
                'ratings': result.get('ratings',0),
                'reviews': result.get('reciews',0),
                'installs': result.get('installs','N/A')
            }
        except Exception as e:
            print(f"Error getting app info for {app_id}:{str(e)}")
            return None

    def scrape_reviews(self, app_id, count=400):
        print(f"\nScraping reviews for {app_id}...")

        for attempts in range(self.max_retries):
            try:
                result, _ = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=count
                )
                print(f"Successfully scraped {len(result)} reviews")
                return result
            except Exception as e:
                print(f"Error scraping reviews for {app_id} (Attempt {attempts + 1}/{self.max_retries}): {str(e)}")
                
                if attempts == self.max_retries - 1:
                    print(f"Retrying in 5 seconds ...")
                    time.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    print(f"Failed to scrape reviews after {self.max_retries} attempts.")
                    return []
                
        return []

    def process_reviews(self, reviews_data, bank_code):
        processed= []
        for review in reviews_data:
            processed.append({
                'review_id': review.get('reviewId',''),
                'review_text': review.get('content',''),
                'rating': review.get('score',0),
                'review_date': review.get('at',datetime.now()),
                'user_name': review.get('userName',''),
                'thumbs_up': review.get('thumbsUpCount',0),
                'bank_code': bank_code,
                'bank_name': self.bank_names[bank_code],
                'app_id': review.get('reviewCreatedVersion','N/A'),
                'source': 'Google Play Store'
            })
        
        return processed
    
    