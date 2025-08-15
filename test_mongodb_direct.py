#!/usr/bin/env python3
"""
Direct MongoDB connection test
"""

from pymongo import MongoClient
import os

def test_mongodb_direct():
    """Test direct connection to MongoDB"""
    print("🔍 Testing direct MongoDB connection...")
    
    try:
        # Test both internal and external connections
        for uri, name in [
            ('mongodb://127.0.0.1:27018/', 'External (127.0.0.1:27018)'),
            ('mongodb://localhost:27017/', 'Internal (localhost:27017)')
        ]:
            print(f"\n📡 Testing {name}: {uri}")
            try:
                client = MongoClient(uri, maxPoolSize=50, connectTimeoutMS=3000, serverSelectionTimeoutMS=3000)
                
                # Test connection
                client.admin.command('ping')
                print(f"✅ Connection successful!")
                
                # Get database
                db = client['bigdata_project']
                print(f"📂 Database: bigdata_project")
                
                # List collections
                collections = db.list_collection_names()
                print(f"📋 Collections: {collections}")
                
                if 'tweets' in collections:
                    count = db.tweets.estimated_document_count()
                    print(f"📊 Tweet count (estimated): {count}")
                    
                    if count == 0:
                        count = db.tweets.count_documents({})
                        print(f"📊 Tweet count (exact): {count}")
                    
                    # Sample one document
                    sample = db.tweets.find_one()
                    if sample:
                        print(f"📝 Sample document keys: {list(sample.keys())}")
                        if 'tweet' in sample:
                            tweet_text = sample['tweet']
                            print(f"📝 Sample tweet (first 100 chars): {str(tweet_text)[:100]}...")
                else:
                    print(f"❌ 'tweets' collection not found!")
                    
                client.close()
                return True
                
            except Exception as e:
                print(f"❌ Connection failed: {e}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_mongodb_direct()
