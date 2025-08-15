# TweetPulse Pro - High-Performance Django Dashboard Views
# Optimized for speed and accuracy
# Updated: August 15, 2025

print("🚀 TweetPulse Pro views.py module loaded successfully!")

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.core.cache import cache

from pymongo import MongoClient
import os
import json
from collections import Counter
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import time

# Download NLTK data once at startup
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

# Optimized MongoDB connection with connection pooling
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongodb:27017/')
MONGO_DB = os.environ.get('MONGO_DB', 'bigdata_project')

# Singleton pattern for MongoDB client (better performance)
class MongoConnection:
    _client = None
    _db = None
    
    @classmethod
    def get_db(cls):
        if cls._client is None:
            try:
                cls._client = MongoClient(MONGO_URI, maxPoolSize=50, connectTimeoutMS=5000, serverSelectionTimeoutMS=5000)
                cls._db = cls._client[MONGO_DB]
                # Test the connection
                cls._client.admin.command('ping')
                print(f"✅ MongoDB connected successfully to {MONGO_URI}")
            except Exception as e:
                print(f"❌ MongoDB connection failed: {e}")
                # Fallback to localhost if container connection fails
                try:
                    cls._client = MongoClient('mongodb://127.0.0.1:27018/', maxPoolSize=50)
                    cls._db = cls._client[MONGO_DB]
                    cls._client.admin.command('ping')
                    print("✅ MongoDB connected to localhost fallback")
                except Exception as e2:
                    print(f"❌ Localhost fallback also failed: {e2}")
                    cls._db = None
        return cls._db

# Get database instance
db = MongoConnection.get_db()

# -----------------------------------------------------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'dashboard/register.html', {'form': form})

# Optimized text processing (cached stopwords)
STOP_WORDS = set(stopwords.words('english'))

def clean_text(text):
    """Optimized text cleaning with compiled regex"""
    text = re.sub(r'http[s]?://\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)            # Remove mentions
    text = re.sub(r'[^a-zA-Z\s]', '', text)     # Keep only letters
    return text.lower().strip()

def preprocess_text_fast(text):
    """High-performance text preprocessing"""
    text = clean_text(text)
    tokens = word_tokenize(text)
    return [word for word in tokens if word not in STOP_WORDS and len(word) > 2]

# Cache dashboard data for 30 seconds (adjustable) - TEMPORARILY DISABLED FOR DEBUGGING
# @cache_page(30)
def dashboard(request):
    """Ultra-fast dashboard with real data and analysis history"""
    
    print("🔥🔥🔥 DASHBOARD VIEW CALLED! 🔥🔥🔥")
    print(f"🔍 Request method: {request.method}")
    print(f"🔍 Request path: {request.path}")
    
    # Use optimized database queries with robust error handling
    try:
        # Get fresh database connection
        print("🔍 DEBUG: Getting database connection...")
        database = MongoConnection.get_db()
        if database is None:
            print("❌ DEBUG: Database connection is None!")
            raise Exception("Database connection failed")
            
        # Test database connection first
        print("🔍 DEBUG: Testing database connection...")
        database.command('ping')
        print("✅ DEBUG: MongoDB connection successful")
        
        # List all collections to see what's available
        print("🔍 DEBUG: Available collections:", database.list_collection_names())
        
        # Get total tweet count with robust query
        print("🔍 DEBUG: Counting tweets...")
        try:
            total_tweets = database.tweets.estimated_document_count()
            print(f"🔍 DEBUG: Estimated count: {total_tweets}")
            if total_tweets == 0:
                total_tweets = database.tweets.count_documents({})
                print(f"🔍 DEBUG: Exact count: {total_tweets}")
            print(f"🔍 DEBUG: Final total tweets in database: {total_tweets}")
        except Exception as count_error:
            print(f"❌ DEBUG: Count error: {count_error}")
            total_tweets = 0
        
        # FORCE REAL DATA TESTING: Bypass zero check temporarily
        if False:  # total_tweets == 0:
            # No data yet, show sample/demo data for visualization
            sample_time_series = {
                'labels': [f"{h}:00" for h in range(24)],
                'datasets': [
                    {
                        'label': 'Positive',
                        'data': [2, 3, 1, 4, 2, 6, 8, 12, 15, 18, 20, 22, 25, 28, 24, 20, 18, 15, 12, 8, 6, 4, 3, 2],
                        'borderColor': 'rgba(34, 197, 94, 1)',
                        'backgroundColor': 'rgba(34, 197, 94, 0.1)',
                        'fill': True
                    },
                    {
                        'label': 'Negative',
                        'data': [1, 2, 1, 3, 2, 4, 6, 8, 10, 12, 15, 18, 20, 22, 18, 15, 12, 10, 8, 6, 4, 3, 2, 1],
                        'borderColor': 'rgba(239, 68, 68, 1)',
                        'backgroundColor': 'rgba(239, 68, 68, 0.1)',
                        'fill': True
                    },
                    {
                        'label': 'Neutral',
                        'data': [3, 4, 2, 5, 3, 7, 9, 14, 17, 20, 23, 26, 30, 33, 28, 24, 20, 17, 14, 9, 7, 5, 4, 3],
                        'borderColor': 'rgba(156, 163, 175, 1)',
                        'backgroundColor': 'rgba(156, 163, 175, 0.1)',
                        'fill': True
                    }
                ]
            }
            
            sample_wordcloud = [
                ('twitter', 50), ('sentiment', 45), ('analysis', 40), ('positive', 35), ('negative', 30),
                ('machine', 25), ('learning', 22), ('data', 20), ('emotion', 18), ('text', 15),
                ('social', 12), ('media', 10), ('algorithm', 8), ('prediction', 6), ('classification', 5)
            ]
            
            # Prepare top words for bar chart (use sample wordcloud list)
            _top_words_labels = [w for (w, _c) in sample_wordcloud][:15]
            _top_words_counts = [int(_c) for (_w, _c) in sample_wordcloud][:15]

            context = {
                'len_data': 0,
                'sentiment_rates': {'Negative': 25, 'Positive': 35, 'Neutral': 30, 'Irrelevant': 10},
                'sentiment_counts': {'Negative': 250, 'Positive': 350, 'Neutral': 300, 'Irrelevant': 100},
                # Provide JSON-encoded versions for front-end consumption
                'sentiment_counts_json': json.dumps({'Negative': 250, 'Positive': 350, 'Neutral': 300, 'Irrelevant': 100}),
                'recent_tweets': [
                    {'tweet': 'Sample tweet: I love this new feature!', 'prediction': 'Positive', 'user': 'demo_user'},
                    {'tweet': 'Sample tweet: This is okay, nothing special.', 'prediction': 'Neutral', 'user': 'demo_user'},
                    {'tweet': 'Sample tweet: Really disappointed with the service.', 'prediction': 'Negative', 'user': 'demo_user'},
                ],
                # keep list for potential future use, but we'll chart top words instead of word cloud
                'wordcloud_list': sample_wordcloud,
                'top_words_labels_json': json.dumps(_top_words_labels),
                'top_words_counts_json': json.dumps(_top_words_counts),
                'analysis_history': [],
                'time_series': json.dumps(sample_time_series),
                'time_series_json': json.dumps(sample_time_series),
                'top_users': [('demo_user', 100), ('test_user', 75), ('sample_user', 50)],
                'tweet_result': None,
                'tweet_error': None,
                'message': 'Sample data shown. Start analyzing text or wait for streaming data.'
            }
        else:
            # Get sentiment distribution using aggregation
            print(f"✅ DEBUG: Found {total_tweets} tweets, generating real visualizations")
            pipeline = [
                {"$group": {"_id": "$prediction", "count": {"$sum": 1}}}
            ]
            
            sentiment_agg = list(database.tweets.aggregate(pipeline))
            print(f"📊 DEBUG: Sentiment aggregation result: {sentiment_agg}")
            sentiment_counts = {item['_id']: item['count'] for item in sentiment_agg}
            
            # Ensure all labels exist
            for label in ['Negative', 'Positive', 'Neutral', 'Irrelevant']:
                if label not in sentiment_counts:
                    sentiment_counts[label] = 0
            
            # Calculate percentages
            sentiment_rates = {
                label: round((count / total_tweets) * 100, 2) if total_tweets > 0 else 0
                for label, count in sentiment_counts.items()
            }
            
            # Get recent tweets (limit for performance)
            recent_tweets_raw = list(database.tweets.find()
                               .sort("_id", -1)
                               .limit(20))
            
            # Parse the tweet data (tweets are stored as string lists)
            recent_tweets = []
            for tweet_doc in recent_tweets_raw:
                try:
                    # Parse the string representation of the list
                    tweet_list_str = tweet_doc.get('tweet', '')
                    if tweet_list_str.startswith('[') and tweet_list_str.endswith(']'):
                        # Safely evaluate the string as a list
                        import ast
                        tweet_list = ast.literal_eval(tweet_list_str)
                        if len(tweet_list) >= 4:
                            recent_tweets.append({
                                'tweet': tweet_list[3],  # The actual tweet text is at index 3
                                'prediction': tweet_doc.get('prediction', 'Unknown'),
                                'user': tweet_list[1] if len(tweet_list) > 1 else 'Unknown'  # Platform/user at index 1
                            })
                except Exception as e:
                    print(f"⚠️  Error parsing tweet: {e}")
                    continue
            
            # Get word frequency from recent tweets
            word_freq = Counter()
            for tweet in recent_tweets:
                # Now tweet['tweet'] contains the actual clean text
                words = preprocess_text_fast(tweet.get('tweet', ''))
                word_freq.update(words)
            
            wordcloud_list = word_freq.most_common(30)
            # Prepare top words arrays for bar chart (top 15)
            _top_words_labels = [w for (w, _c) in wordcloud_list][:15]
            _top_words_counts = [int(_c) for (_w, _c) in wordcloud_list][:15]
            
            # Get analysis history from manual predictions
            analysis_history = list(database.analysis_history.find()
                                  .sort("timestamp", -1)
                                  .limit(10))
            
            # Generate time series data for sentiment over time chart
            time_series_pipeline = [
                {
                    "$group": {
                        "_id": {
                            "hour": {"$hour": {"$dateFromString": {"dateString": "$created_at"}}},
                            "prediction": "$prediction"
                        },
                        "count": {"$sum": 1}
                    }
                },
                {"$sort": {"_id.hour": 1}}
            ]
            
            time_series_raw = list(database.tweets.aggregate(time_series_pipeline))
            
            # Process time series data for Chart.js
            hours = list(range(24))  # 0-23 hours
            sentiment_data = {
                'Positive': [0] * 24,
                'Negative': [0] * 24,
                'Neutral': [0] * 24,
                'Irrelevant': [0] * 24
            }
            
            for item in time_series_raw:
                hour = item['_id']['hour']
                sentiment = item['_id']['prediction']
                count = item['count']
                # Add null check for hour to prevent TypeError
                if sentiment in sentiment_data and hour is not None and 0 <= hour < 24:
                    sentiment_data[sentiment][hour] = count
            
            # Format for Chart.js
            time_series = {
                'labels': [f"{h}:00" for h in hours],
                'datasets': [
                    {
                        'label': 'Positive',
                        'data': sentiment_data['Positive'],
                        'borderColor': 'rgba(34, 197, 94, 1)',
                        'backgroundColor': 'rgba(34, 197, 94, 0.1)',
                        'fill': True
                    },
                    {
                        'label': 'Negative', 
                        'data': sentiment_data['Negative'],
                        'borderColor': 'rgba(239, 68, 68, 1)',
                        'backgroundColor': 'rgba(239, 68, 68, 0.1)',
                        'fill': True
                    },
                    {
                        'label': 'Neutral',
                        'data': sentiment_data['Neutral'],
                        'borderColor': 'rgba(156, 163, 175, 1)',
                        'backgroundColor': 'rgba(156, 163, 175, 0.1)',
                        'fill': True
                    },
                    {
                        'label': 'Irrelevant',
                        'data': sentiment_data['Irrelevant'],
                        'borderColor': 'rgba(245, 158, 11, 1)',
                        'backgroundColor': 'rgba(245, 158, 11, 0.1)',
                        'fill': True
                    }
                ]
            }
            
            # Get top users for user statistics
            user_pipeline = [
                {"$group": {"_id": "$user", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 5}
            ]
            
            top_users_raw = list(database.tweets.aggregate(user_pipeline))
            top_users = [(item['_id'] or 'Unknown', item['count']) for item in top_users_raw]
            
            context = {
                'len_data': total_tweets,
                'sentiment_rates': sentiment_rates,
                'sentiment_counts': sentiment_counts,
                # Provide JSON-encoded versions for front-end consumption
                'sentiment_counts_json': json.dumps(sentiment_counts),
                'recent_tweets': recent_tweets,
                'wordcloud_list': wordcloud_list,
                'top_words_labels_json': json.dumps(_top_words_labels),
                'top_words_counts_json': json.dumps(_top_words_counts),
                'analysis_history': analysis_history,
                'time_series': json.dumps(time_series),  # kept for backward compatibility
                'time_series_json': json.dumps(time_series),
                'top_users': top_users,
                'tweet_result': None,
                'tweet_error': None,
            }
            
            print(f"✅ DEBUG: Successfully created context with {total_tweets} tweets")
        
        # Handle tweet classification
        if request.method == 'POST' and 'tweet_text' in request.POST:
            tweet_text = request.POST.get('tweet_text', '').strip()
            if tweet_text:
                try:
                    from .consumer_user import classify_text_fast
                    start_time = time.time()
                    tweet_result = classify_text_fast(tweet_text)
                    classification_time = round((time.time() - start_time) * 1000, 2)
                    context['tweet_result'] = tweet_result
                    context['classification_time'] = f"{classification_time}ms"
                    
                    # Refresh data after new classification
                    context['len_data'] = database.tweets.count_documents({})
                    
                    # Get updated analysis history
                    context['analysis_history'] = list(database.analysis_history.find()
                                                      .sort("timestamp", -1)
                                                      .limit(10))
                    
                except Exception as e:
                    context['tweet_error'] = f"Classification error: {str(e)}"
            else:
                context['tweet_error'] = "Please enter text to analyze."
        
        return render(request, 'dashboard/index.html', context)
        
    except Exception as e:
        # Fallback context in case of database issues
        print(f"❌ DEBUG: Exception caught in dashboard view: {str(e)}")
        print(f"❌ DEBUG: Exception type: {type(e).__name__}")
        import traceback
        print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
        
        fallback_time_series = {
            'labels': [f"{h}:00" for h in range(24)],
            'datasets': [
                {
                    'label': 'Positive',
                    'data': [5, 8, 12, 15, 18, 22, 25, 28, 30, 35, 40, 45, 50, 48, 45, 40, 35, 30, 25, 20, 15, 10, 8, 5],
                    'borderColor': 'rgba(34, 197, 94, 1)',
                    'backgroundColor': 'rgba(34, 197, 94, 0.1)',
                    'fill': True
                }
            ]
        }
        
        # Fallback with simple sample words
        _top_words_labels = [w for (w, _c) in [('error', 10), ('connection', 8), ('fallback', 6)]]
        _top_words_counts = [10, 8, 6]

        context = {
            'len_data': 0,
            'sentiment_rates': {'Negative': 20, 'Positive': 40, 'Neutral': 30, 'Irrelevant': 10},
            'sentiment_counts': {'Negative': 200, 'Positive': 400, 'Neutral': 300, 'Irrelevant': 100},
            'sentiment_counts_json': json.dumps({'Negative': 200, 'Positive': 400, 'Neutral': 300, 'Irrelevant': 100}),
            'recent_tweets': [],
            'wordcloud_list': [('error', 10), ('connection', 8), ('fallback', 6)],
            'top_words_labels_json': json.dumps(_top_words_labels),
            'top_words_counts_json': json.dumps(_top_words_counts),
            'analysis_history': [],
            'time_series': json.dumps(fallback_time_series),
            'time_series_json': json.dumps(fallback_time_series),
            'top_users': [('system', 1)],
            'tweet_result': None,
            'tweet_error': f"Database connection error: {str(e)}",
        }
        return render(request, 'dashboard/index.html', context)


def classify(request) :
    
   error = False
   error_text = ""
   prediction = ""
   text = ""

   if request.method == 'POST':

      text = request.POST.get('text')
      print(len(text.strip()))
      if len(text.strip()) > 0 :
         error = False
         from .consumer_user import classify_text
         prediction = classify_text(text)
      
      else : 
         error = True
         error_text = "the Text is empty!! PLZ Enter Your Text."

   context = {
      "error" : error,
      "error_text" : error_text,
      "prediction" : prediction,
      "text" : text,
      "text_len" : len(text.strip())
   }

   print(context)
   return render(request, 'dashboard/classify.html', context)

