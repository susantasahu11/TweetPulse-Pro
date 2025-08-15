#!/usr/bin/env python3
"""
Test to check the dashboard output and visualizations
"""

import requests
import json

def test_dashboard_response():
    """Test the actual dashboard response"""
    print("🔍 Testing TweetPulse Pro Dashboard Response...")
    
    try:
        # Test main dashboard
        response = requests.get("http://localhost:8000", allow_redirects=True, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response length: {len(response.text)} characters")
        
        # Check if it's showing real data or sample data
        content = response.text
        
        # Check for key indicators
        indicators = {
            "Chart.js": "Chart.js" in content,
            "WordCloud": "WordCloud" in content or "wordcloud" in content,
            "sentimentPieChart": "sentimentPieChart" in content,
            "sentimentTimeSeries": "sentimentTimeSeries" in content,
            "Sample data shown": "Sample data shown" in content,
            "Recent Tweets": "Recent Tweets" in content,
            "Sentiment Distribution": "Sentiment Distribution" in content,
            "Analysis History": "Analysis History" in content,
            "JSON.parse": "JSON.parse" in content,
            "timeSeries.labels": "timeSeries.labels" in content,
        }
        
        print("\n📊 Content Analysis:")
        for indicator, found in indicators.items():
            status = "✅" if found else "❌"
            print(f"   {status} {indicator}")
        
        # Check if there's actual data in JavaScript
        if "var sentimentCounts = JSON.parse" in content:
            print("\n📈 Sentiment data found in JavaScript!")
        
        if "var timeSeries = JSON.parse" in content:
            print("📈 Time series data found in JavaScript!")
        
        # Look for error messages
        if "error" in content.lower() or "empty" in content.lower():
            print("\n⚠️  Possible errors or empty data indicators found")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_dashboard_response()
