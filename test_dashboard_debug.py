#!/usr/bin/env python3
"""
Test to directly debug the Django view database access
"""

import requests
import time

def test_dashboard_debug():
    """Force a request and check logs for our debug output"""
    print("🔍 Testing Dashboard Debug Output...")
    
    # Make a request to trigger the view
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        print(f"📊 Response: {response.status_code} ({len(response.text)} chars)")
        
        # Wait a moment for logs to appear
        time.sleep(2)
        
        # Now check if our debug output appears
        print("✅ Request sent. Check the logs for debug output manually.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_dashboard_debug()
