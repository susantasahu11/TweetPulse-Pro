#!/usr/bin/env python3
"""
TweetPulse Pro - Performance Test Script
Test classification speed and verify data population
"""
import requests
import time
import json

def test_classification_speed():
    """Test the classification endpoint for speed"""
    test_texts = [
        "I love this amazing product! It's fantastic!",
        "This is terrible and I hate it completely.",
        "The weather is okay today, nothing special.",
        "Check out this random link http://example.com"
    ]
    
    print("🚀 TweetPulse Pro - Performance Testing")
    print("=" * 50)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}: {text[:30]}...")
        
        # Test classification via POST to dashboard
        start_time = time.time()
        
        try:
            response = requests.post(
                'http://localhost:8000/',
                data={'tweet_text': text},
                timeout=10,
                allow_redirects=True
            )
            
            end_time = time.time()
            duration = round((end_time - start_time) * 1000, 2)
            
            if response.status_code == 200:
                print(f"✅ Classification completed in {duration}ms")
            else:
                print(f"⚠️  HTTP {response.status_code} - {duration}ms")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test API endpoints
    print(f"\n📊 API Performance Tests")
    print("-" * 30)
    
    api_endpoints = [
        ('Tweets API', 'http://localhost:5000/api/tweets?limit=10'),
        ('Stats API', 'http://localhost:5000/api/stats'),
        ('API Docs', 'http://localhost:5000/api/docs')
    ]
    
    for name, url in api_endpoints:
        start_time = time.time()
        try:
            response = requests.get(url, timeout=5)
            end_time = time.time()
            duration = round((end_time - start_time) * 1000, 2)
            
            if response.status_code == 200:
                print(f"✅ {name}: {duration}ms")
                if 'api/' in url and url.endswith('stats'):
                    data = response.json()
                    print(f"   Data: {data}")
            else:
                print(f"⚠️  {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {e}")

if __name__ == "__main__":
    test_classification_speed()
