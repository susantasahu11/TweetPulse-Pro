#!/usr/bin/env python3
"""
Final comprehensive test to diagnose the dashboard issue
"""

import requests
from bs4 import BeautifulSoup

def test_dashboard_content():
    """Test the actual dashboard content in detail"""
    print("🔍 Final Dashboard Diagnosis...")
    
    try:
        # Get the dashboard
        response = requests.get("http://localhost:8000", allow_redirects=True, timeout=10)
        print(f"📊 Status: {response.status_code}")
        print(f"📏 Length: {len(response.text)} characters")
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for specific indicators
        recent_tweets_section = soup.find(text="Recent Tweets")
        user_stats_section = soup.find(text="User Statistics")
        analysis_history = soup.find(text="Your Analysis History")
        
        print(f"\n🔍 Content Analysis:")
        print(f"   Recent Tweets section: {'✅ Found' if recent_tweets_section else '❌ Missing'}")
        print(f"   User Statistics section: {'✅ Found' if user_stats_section else '❌ Missing'}")
        print(f"   Analysis History section: {'✅ Found' if analysis_history else '❌ Missing'}")
        
        # Check for tables with actual data
        tables = soup.find_all('table')
        print(f"   Number of tables: {len(tables)}")
        
        for i, table in enumerate(tables):
            rows = table.find_all('tr')
            print(f"   Table {i+1}: {len(rows)} rows")
            
        # Check for specific data indicators
        if "demo_user" in response.text:
            print("   📋 Sample/demo data detected")
        
        if "Sample data shown" in response.text:
            print("   📋 'Sample data shown' message found")
            
        if "len_data != 0" in response.text:
            print("   📋 Template logic visible in output")
            
        # Check JavaScript data
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string and 'sentimentCounts' in script.string:
                print("   📈 Sentiment data in JavaScript found")
                # Extract sentiment counts
                if 'JSON.parse' in script.string:
                    start = script.string.find("JSON.parse('") + 12
                    end = script.string.find("')", start)
                    if start < end:
                        sentiment_data = script.string[start:end]
                        print(f"   📊 Sentiment data: {sentiment_data[:100]}...")
                        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_dashboard_content()
