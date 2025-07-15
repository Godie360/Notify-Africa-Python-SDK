#!/usr/bin/env python3
"""
Debug script to test Notify Africa API endpoints and identify issues
"""

import os
import requests
import json
from notify_africa import NotifyAfricaClient
from notify_africa.exceptions import *

def test_direct_api_call():
    """Test direct API call to see raw response"""
    print("=== Testing Direct API Call ===")
    
    api_key = os.getenv("NOTIFY_AFRICA_API_KEY")
    base_url = "https://api.notify.africa/v2"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Test profile endpoint first (lowest cost)
    url = f"{base_url}/api/profile"
    
    try:
        print(f"Making request to: {url}")
        print(f"Headers: {json.dumps({k: v[:50] + '...' if len(v) > 50 else v for k, v in headers.items()}, indent=2)}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Raw Response: {response.text}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                data = response.json()
                print(f"JSON Response: {json.dumps(data, indent=2)}")
            except:
                print("Could not parse JSON response")
                
        return response.status_code == 200
        
    except Exception as e:
        print(f"Request failed: {e}")
        return False

def test_sdk_with_debug():
    """Test SDK with enhanced error reporting"""
    print("\n=== Testing SDK with Debug Info ===")
    
    client = NotifyAfricaClient(
        api_key=os.getenv("NOTIFY_AFRICA_API_KEY"),
        sender_id=os.getenv("NOTIFY_AFRICA_SENDER_ID")
    )
    
    try:
        print("Testing get_profile()...")
        profile = client.get_profile()
        print(f"✅ Profile success: {json.dumps(profile, indent=2)}")
        return True
        
    except Exception as e:
        print(f"❌ Profile failed: {e}")
        print(f"Exception type: {type(e).__name__}")
        
        # Print additional error details if available
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")
        if hasattr(e, 'response_data'):
            print(f"Response data: {e.response_data}")
        
        return False

def test_different_endpoints():
    """Test different possible API endpoint formats"""
    print("\n=== Testing Different Endpoint Formats ===")
    
    api_key = os.getenv("NOTIFY_AFRICA_API_KEY")
    
    endpoints = [
        "https://api.notify.africa/v2/api/profile",
        "https://api.notify.africa/api/profile", 
        "https://api.notifyafrica.com/v2/api/profile",
        "https://notifyafrica.com/api/v2/profile",
        "https://api.notify.africa/v2/profile",
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    for url in endpoints:
        try:
            print(f"\nTesting: {url}")
            response = requests.get(url, headers=headers, timeout=5)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f" SUCCESS! Working endpoint: {url}")
                try:
                    data = response.json()
                    print(f"  Response: {json.dumps(data, indent=4)}")
                except:
                    print(f"  Response (text): {response.text}")
                return url
            else:
                print(f"  Response: {response.text[:200]}")
                
        except Exception as e:
            print(f" Error: {e}")
    
    return None

def test_authentication_formats():
    """Test different authentication header formats"""
    print("\n=== Testing Authentication Formats ===")
    
    api_key = os.getenv("NOTIFY_AFRICA_API_KEY")
    url = "https://api.notify.africa/v2/api/profile"
    
    auth_formats = [
        {"Authorization": f"Bearer {api_key}"},
        {"Authorization": f"Token {api_key}"},
        {"X-API-Key": api_key},
        {"Authorization": api_key},
    ]
    
    for i, auth in enumerate(auth_formats, 1):
        try:
            headers = {"Content-Type": "application/json", "Accept": "application/json", **auth}
            print(f"\n{i}. Testing auth format: {list(auth.keys())[0]}")
            
            response = requests.get(url, headers=headers, timeout=5)
            print(f"   Status: {response.status_code}")
            
            if response.status_code < 400:
                print(f" Success with {list(auth.keys())[0]}")
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=4)}")
                except:
                    print(f"   Response: {response.text}")
                return auth
            else:
                print(f"   Response: {response.text[:100]}")
                
        except Exception as e:
            print(f" Error: {e}")
    
    return None

def main():
    print("Notify Africa API Debug Tool")
    print("=" * 50)
    
    # Check environment variables
    api_key = os.getenv("NOTIFY_AFRICA_API_KEY")
    sender_id = os.getenv("NOTIFY_AFRICA_SENDER_ID")
    
    if not api_key:
        print(" NOTIFY_AFRICA_API_KEY not set!")
        return
    
    if not sender_id:
        print("NOTIFY_AFRICA_SENDER_ID not set!")
        return
    
    print(f"✅ API Key: {api_key[:20]}...")
    print(f"✅ Sender ID: {sender_id}")
    
    # Run tests
    success = test_direct_api_call()
    
    if not success:
        print("\nDirect API call failed. Testing different endpoints...")
        working_endpoint = test_different_endpoints()
        
        if not working_endpoint:
            print("\nNo working endpoints found. Testing authentication formats...")
            working_auth = test_authentication_formats()
    
    # Test SDK
    test_sdk_with_debug()
    
    print("\n" + "=" * 50)
    print("Debug complete!")

if __name__ == "__main__":
    main()