import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from datetime import datetime
import re 
from config import DATA_PATHS

class ReviewPreprocessor:
    
    def __init__(self, input_path=None, output_path=None):
        self.input_path= input_path or DATA_PATHS['raw_reviews']
        self.output_path= output_path or DATA_PATHS['processed_reviews']
        self.df=None
        self.stats={}
    
    def load_data(self):
        print("loading data... ")
        try:
            self.df=pd.read_csv(self.input_path)
            print(f"Loaded {len(self.df)} reviews")
            self.stats['initial_count']=len(self.df)
            return True
        except FileNotFoundError:
            print(f"File not found: {self.input_path}")
            return False
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def check_missing_data(self):
        print("\n[1/6] Checking for missing data...")
        missing=self.df.isnull().sum()
        missing_pct=(missing/len(self.df))*100

        print("\nMissing values")
        for col in missing.index:
            if missing[col]>0:
                print(f"{col}: {missing[col]} ({missing_pct[col]:.2f}%)")
        self.stats['missing_values']=missing.to_dict()

        critical_cols=['reviews_text','rating', 'bank_name']
        missing_critical=self.df[critical_cols].isnull().sum()
        if missing_critical.sum()>0:
            print("\nWARNING: Missing values in critical columns: ")
            print(missing_critical[missing_critical>0])
        
    def handle_missing_data(self):
        print("\n[2/6] Handling missing data...")
        
        critical_cols=['reviews_text','rating', 'bank_name']
        before_count=len(self.df)
        self.df=self.df.dropna(subset=critical_cols)
        removed =before_count-len(self.df)

        if removed>0:
            print(f"Removed {removed} reviews with missing critical data")

        self.df['username'] = self.df['user_name'].fillna('Anonymous')
        self.self.df['thumbs_up'] = self.df['thumbs_up'].fillna(0)
        self.df['reply_context'] = self.df['reply_context'].fillna('')

        self.stats['rows_removed_missing'] = removed
        self.stats['count_after_missing']=len(self.df)

    def normalize_date(self):

        print("\n[3/6] Normalizing review dates...")
        
        try:
            self.df['review_date']=pd.to_datetime(self.df['review_date'])
            self.df['review_date']=self.df['review_date'].dt.date
            self.df['review_year']=pd.to_datetime(self.df['review_date']).dt.year
            self.df['review_month']=pd.to_datetime(self.df['review_date']).dt.month

            print(f"Date range:{self.df['review_date'].min()} to {self.df['review_date'].max()}")
        except Exception as e:
            print(f"WARNING: Error normalizing dates: {str(e)}")
    