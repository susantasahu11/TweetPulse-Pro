#!/usr/bin/env python3
"""
Test authenticated dashboard access
"""

import requests
from bs4 import BeautifulSoup

def test_authenticated_dashboard():
    """Test the dashboard with authentication"""
    print("🔐 Testing Authenticated Dashboard Access...")
    
    # Create a session
    session = requests.Session()
    
    try:
        # Get the login page
        print("📋 Getting login page...")
        login_url = "http://localhost:8000/accounts/login/"
        login_page = session.get(login_url)
        
        # Parse CSRF token
        soup = BeautifulSoup(login_page.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        print(f"🔑 CSRF Token: {csrf_token[:10]}...")
        
        # Try to create a test user first via register
        print("👤 Attempting to register test user...")
        register_url = "http://localhost:8000/register/"
        register_page = session.get(register_url)
        soup = BeautifulSoup(register_page.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        
        register_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': 'testuser',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        
        register_response = session.post(register_url, data=register_data)
        print(f"📝 Register response: {register_response.status_code}")
        
        # Now try to login
        print("🔓 Attempting login...")
        login_page = session.get(login_url)
        soup = BeautifulSoup(login_page.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        
        login_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': 'testuser',
            'password': 'testpass123!'
        }
        
        login_response = session.post(login_url, data=login_data)
        print(f"🔐 Login response: {login_response.status_code}")
        
        # Now access the dashboard
        print("📊 Accessing authenticated dashboard...")
        dashboard_response = session.get("http://localhost:8000/")
        print(f"📋 Dashboard response: {dashboard_response.status_code}")
        print(f"📏 Response length: {len(dashboard_response.text)} characters")
        
        # Check for real data indicators
        content = dashboard_response.text
        
        if "Recent Tweets" in content and "demo_user" not in content:
            print("✅ Real tweet data detected!")
        elif "Sample data shown" in content:
            print("❌ Still showing sample data")
        else:
            print("🔍 Data status unclear")
            
        # Look for JavaScript data
        if "var sentimentCounts" in content:
            print("✅ Sentiment data present in JavaScript")
        if "var timeSeries" in content:
            print("✅ Time series data present in JavaScript")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_authenticated_dashboard()
