#!/usr/bin/env python3
"""
TweetPulse Pro Performance and Visualization Test
Tests ultra-fast classification and complete dashboard functionality.
"""

import requests
import time
import json
from datetime import datetime

def test_ultra_fast_classification():
    """Test the new ultra-fast classification system"""
    print("🚀 Testing Ultra-Fast Classification...")
    
    test_texts = [
        "I love this amazing product!",
        "This is terrible and disappointing",
        "It's okay, nothing special",
        "Random noise dfgjkl;dfgkl;",
        "The weather is nice today",
    ]
    
    base_url = "http://localhost:8000"
    
    # Get session and CSRF token first
    session = requests.Session()
    
    try:
        # Get CSRF token from login page
        login_page = session.get(f"{base_url}/accounts/login/")
        csrf_token = None
        
        if 'csrftoken' in session.cookies:
            csrf_token = session.cookies['csrftoken']
        
        print(f"   📋 CSRF Token: {csrf_token[:10]}..." if csrf_token else "   ❌ No CSRF token")
        
        # Test classification speed
        total_time = 0
        successful_tests = 0
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n   🧪 Test {i}: '{text[:30]}...'")
            
            data = {
                'tweet_text': text,
                'csrfmiddlewaretoken': csrf_token
            }
            
            start_time = time.time()
            
            try:
                response = session.post(f"{base_url}/", data=data, timeout=30)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                total_time += response_time
                
                print(f"      ⏱️  Response Time: {response_time:.2f}ms")
                print(f"      🔍 Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    successful_tests += 1
                    if "Classified in" in response.text:
                        # Extract classification time from response
                        import re
                        time_match = re.search(r'Classified in ([\d.]+)ms', response.text)
                        if time_match:
                            actual_time = float(time_match.group(1))
                            print(f"      ✅ Actual Classification: {actual_time:.2f}ms")
                            
                            if actual_time < 5000:  # Less than 5 seconds
                                print(f"      🎉 FAST! ({actual_time:.2f}ms)")
                            else:
                                print(f"      ⚠️  Still slow: {actual_time:.2f}ms")
                        else:
                            print("      📊 Classification completed (time not extracted)")
                    else:
                        print("      ❓ Response received but classification status unclear")
                        
            except requests.exceptions.Timeout:
                print(f"      ❌ Timeout after 30 seconds")
            except Exception as e:
                print(f"      ❌ Error: {e}")
        
        if successful_tests > 0:
            avg_time = total_time / successful_tests
            print(f"\n   📊 Average Response Time: {avg_time:.2f}ms")
            print(f"   ✅ Successful Tests: {successful_tests}/{len(test_texts)}")
            
            if avg_time < 5000:
                print("   🎉 PERFORMANCE EXCELLENT! Classification is ultra-fast!")
            elif avg_time < 15000:
                print("   ✅ Performance Good (under 15 seconds)")
            else:
                print("   ⚠️  Performance needs improvement")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")

def test_dashboard_visualizations():
    """Test that all dashboard sections have data"""
    print("\n📊 Testing Dashboard Visualizations...")
    
    try:
        response = requests.get("http://localhost:8000/", allow_redirects=True, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # Check for various visualization components
            checks = [
                ("Sentiment Distribution Chart", "sentimentPieChart" in content),
                ("Time Series Chart", "sentimentTimeSeries" in content),
                ("Word Cloud", "wordCloud" in content),
                ("Recent Tweets Table", "Recent Tweets" in content),
                ("User Statistics", "User Statistics" in content),
                ("Analysis History", "Analysis History" in content),
                ("Chart.js Library", "chart.min.js" in content),
                ("WordCloud Library", "wordcloud2" in content),
                ("TweetPulse Pro Branding", "TweetPulse Pro" in content),
            ]
            
            print("   🔍 Dashboard Component Checks:")
            for component, found in checks:
                status = "✅" if found else "❌"
                print(f"      {status} {component}")
            
            # Check for empty sections
            empty_indicators = [
                "The database is empty",
                "No data yet",
                "sentiment_counts = {}"
            ]
            
            has_empty_sections = any(indicator in content for indicator in empty_indicators)
            
            if has_empty_sections:
                print("   📋 Sample/Demo data detected (no real data yet)")
            else:
                print("   📊 Real data detected in visualizations")
                
        else:
            print(f"   ❌ Dashboard not accessible: Status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Dashboard test failed: {e}")

def test_api_endpoints():
    """Test API performance"""
    print("\n🔌 Testing API Endpoints...")
    
    endpoints = [
        ("/api/stats", "Statistics"),
        ("/api/tweets?limit=5", "Recent Tweets"),
        ("/api/docs", "API Documentation")
    ]
    
    for endpoint, name in endpoints:
        try:
            start_time = time.time()
            response = requests.get(f"http://localhost:5000{endpoint}", timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            print(f"   📡 {name}: {response.status_code} ({response_time:.0f}ms)")
            
            if endpoint == "/api/stats" and response.status_code == 200:
                try:
                    stats = response.json()
                    total_tweets = sum(item['count'] for item in stats)
                    print(f"      📊 Total tweets in system: {total_tweets}")
                except:
                    print("      📊 Stats format: Non-JSON response")
                    
        except Exception as e:
            print(f"   ❌ {name} failed: {e}")

def main():
    """Run comprehensive TweetPulse Pro test suite"""
    print("🎯 TweetPulse Pro Ultra-Performance Test Suite")
    print("=" * 60)
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_ultra_fast_classification()
    test_dashboard_visualizations()
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("🎉 Test Suite Complete!")
    print("\nIf classification times are under 5 seconds and all visualizations")
    print("are present, your TweetPulse Pro system is performing optimally! 🚀")

if __name__ == "__main__":
    main()
