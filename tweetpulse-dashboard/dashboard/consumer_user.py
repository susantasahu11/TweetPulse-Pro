# TweetPulse Pro - Ultra-Fast Text Classification
# Optimized for speed and accuracy

from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
import re
import nltk
import os
from functools import lru_cache
from pymongo import MongoClient
import datetime
import threading

# Download NLTK data once
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

# MongoDB connection for storing analysis history
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.environ.get('MONGO_DB', 'bigdata_project')

# Global instances for maximum speed
_spark_instance = None
_pipeline_instance = None
_initialization_lock = threading.Lock()

def initialize_spark_components():
    """Initialize Spark components once globally"""
    global _spark_instance, _pipeline_instance
    
    if _spark_instance is None:
        with _initialization_lock:
            if _spark_instance is None:  # Double-check locking
                print("🚀 Initializing TweetPulse Pro Spark Engine...")
                _spark_instance = SparkSession.builder \
                    .appName("TweetPulse_UltraFast") \
                    .config("spark.sql.adaptive.enabled", "true") \
                    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
                    .config("spark.driver.memory", "2g") \
                    .config("spark.driver.maxResultSize", "1g") \
                    .getOrCreate()
                _spark_instance.sparkContext.setLogLevel("ERROR")
                
                MODEL_PATH = os.environ.get('MODEL_PATH', 'logistic_regression_model.pkl')
                _pipeline_instance = PipelineModel.load(MODEL_PATH)
                print("✅ TweetPulse Pro Engine Ready!")

# Initialize on module load
initialize_spark_components()

# Pre-compiled regex patterns for maximum performance
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+|\S+\.com\S+|youtu\.be/\S+')
MENTION_HASHTAG_PATTERN = re.compile(r'(@|#)\w+')
NON_ALPHA_PATTERN = re.compile(r'[^a-zA-Z\s]')
WHITESPACE_PATTERN = re.compile(r'\s+')

@lru_cache(maxsize=1000)  # Cache cleaned text for speed
def clean_text_fast(text):
    """Ultra-fast text cleaning with caching"""
    if not text:
        return ''
    
    # Apply all regex patterns
    text = URL_PATTERN.sub('', text)
    text = MENTION_HASHTAG_PATTERN.sub('', text)
    text = text.lower()
    text = NON_ALPHA_PATTERN.sub('', text)
    text = WHITESPACE_PATTERN.sub(' ', text).strip()
    return text
    
class_index_mapping = {0: "Negative", 1: "Positive", 2: "Neutral", 3: "Irrelevant"}

def classify_text_fast(text: str):
    """Ultra-fast text classification with global instances"""
    global _spark_instance, _pipeline_instance
    
    try:
        # Ensure components are initialized
        if _spark_instance is None or _pipeline_instance is None:
            initialize_spark_components()
        
        # Fast text preprocessing
        preprocessed_tweet = clean_text_fast(text)
        
        if not preprocessed_tweet.strip():
            return "Irrelevant"
        
        # Use global instances for maximum speed
        data = _spark_instance.createDataFrame([(preprocessed_tweet,)], ["Text"])
        processed_data = _pipeline_instance.transform(data)
        prediction = processed_data.collect()[0][6]
        sentiment = class_index_mapping[int(prediction)]
        
        # Store in MongoDB asynchronously (don't block classification)
        def store_async():
            try:
                client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=500)
                db = client[MONGO_DB]
                
                # Store in analysis history collection
                history_doc = {
                    "original_text": text,
                    "cleaned_text": preprocessed_tweet,
                    "prediction": sentiment,
                    "timestamp": datetime.datetime.utcnow(),
                    "source": "manual_analysis"
                }
                db.analysis_history.insert_one(history_doc)
                
                # Also store in tweets collection for dashboard data
                tweet_doc = {
                    "tweet": text,
                    "prediction": sentiment,
                    "created_at": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    "user": "Manual Analysis"
                }
                db.tweets.insert_one(tweet_doc)
                
            except Exception as mongo_error:
                print(f"MongoDB storage error: {mongo_error}")
        
        # Start storage in background thread
        storage_thread = threading.Thread(target=store_async, daemon=True)
        storage_thread.start()
        
        return sentiment
        
    except Exception as e:
        print(f"Classification error: {e}")
        return "Error"

# Backward compatibility
def classify_text(text: str):
    """Legacy function wrapper for compatibility"""
    return classify_text_fast(text)