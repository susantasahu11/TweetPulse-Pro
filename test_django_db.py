#!/usr/bin/env python3
"""
Test the exact database query that Django is using
"""

import os
import sys
import django

# Add the Django project to Python path
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BigDataProject.settings')

# Setup Django
django.setup()

from dashboard.views import MongoConnection

def test_django_db():
    """Test the exact database connection Django uses"""
    print("🔍 Testing Django Database Connection...")
    
    try:
        db = MongoConnection.get_db()
        
        # Test exact queries that dashboard uses
        total_tweets = db.tweets.count_documents({})
        print(f"📊 Total tweets via Django: {total_tweets}")
        
        if total_tweets > 0:
            # Test sentiment aggregation
            pipeline = [
                {"$group": {"_id": "$prediction", "count": {"$sum": 1}}}
            ]
            sentiment_agg = list(db.tweets.aggregate(pipeline))
            print(f"📈 Sentiment aggregation: {sentiment_agg}")
            
            # Test recent tweets
            recent_tweets = list(db.tweets.find().sort("_id", -1).limit(5))
            print(f"📝 Recent tweets count: {len(recent_tweets)}")
            if recent_tweets:
                print(f"📝 Sample tweet: {recent_tweets[0].get('tweet', 'N/A')[:50]}...")
                
        else:
            print("❌ No tweets found via Django!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_django_db()
