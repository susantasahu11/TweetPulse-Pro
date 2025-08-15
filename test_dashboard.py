#!/usr/bin/env python3
"""
Quick test to verify TweetPulse Pro dashboard is working correctly.
"""

import requests
import time

def test_dashboard():
    """Test the dashboard endpoints"""
    base_url = "http://localhost:8000"
    
    print("🔥 Testing TweetPulse Pro Dashboard...")
    
    try:
        # Test main dashboard
        print("📊 Testing main dashboard...")
        response = requests.get(base_url, allow_redirects=True, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dashboard loads successfully!")
            if "TweetPulse Pro" in response.text:
                print("   ✅ TweetPulse Pro branding detected!")
            if "Invalid block tag" in response.text:
                print("   ❌ Template syntax error still present!")
            else:
                print("   ✅ No template syntax errors!")
        else:
            print(f"   ❌ Dashboard failed with status {response.status_code}")
            
        # Test login page
        print("\n🔐 Testing login page...")
        login_response = requests.get(f"{base_url}/accounts/login/", timeout=10)
        print(f"   Status: {login_response.status_code}")
        if login_response.status_code == 200:
            print("   ✅ Login page loads successfully!")
        
        # Test classifier page  
        print("\n🤖 Testing classifier page...")
        classify_response = requests.get(f"{base_url}/classify/", timeout=10)
        print(f"   Status: {classify_response.status_code}")
        if classify_response.status_code in [200, 302]:  # 302 if redirected to login
            print("   ✅ Classifier page accessible!")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
        
    print("\n🎉 Dashboard test completed!")
    return True

if __name__ == "__main__":
    test_dashboard()
