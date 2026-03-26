#!/usr/bin/env python3
"""
Comprehensive test of Stock Prediction application
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

print("=" * 60)
print("Stock Prediction Application - Comprehensive Test")
print("=" * 60)

# Test 1: Health Check
print("\n[1] Testing Health Check...")
try:
    r = requests.get(f'{BASE_URL}/health', timeout=5)
    print(f"✓ Status: {r.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Registration
print("\n[2] Testing User Registration...")
try:
    r = requests.post(
        f'{BASE_URL}/auth/register',
        json={'username': 'final_test_user', 'email': 'final@test.com', 'password': 'TestPass123'},
        timeout=5
    )
    if r.status_code == 200:
       print(f"✓ Registration successful: User ID {r.json()['id']}")
    elif r.status_code == 400:
        print(f"✓ User already exists (expected on second run)")
    else:
        print(f"✗ Status: {r.status_code} - {r.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Login
print("\n[3] Testing User Login...")
try:
    r = requests.post(
        f'{BASE_URL}/auth/login?username=test_user_now&password=Test123',
        timeout=5
    )
    if r.status_code == 200:
        token = r.json()['access_token']
        print(f"✓ Login successful")
        print(f"  Token (first 50 chars): {token[:50]}...")
        headers = {'Authorization': f'Bearer {token}'}
    else:
        print(f"✗ Status: {r.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Stock Data
print("\n[4] Testing Stock Data Endpoint...")
try:
    r = requests.get(f'{BASE_URL}/stock/data/NIFTY?days=30', timeout=10)
    if r.status_code == 200:
        data = r.json()
        print(f"✓ Stock data received")
        print(f"  Ticker: {data['ticker']}")
        print(f"  Records: {len(data['data'])}")
        if data['data']:
            print(f"  First: {data['data'][0]['date']} - Close: ${data['data'][0]['close']:.2f}")
    else:
        print(f"✗ Status: {r.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 5: Sentiment Analysis
print("\n[5] Testing Sentiment Analysis...")
try:
    r = requests.get(f'{BASE_URL}/sentiment/NIFTY', timeout=10)
    if r.status_code == 200:
        data = r.json()
        print(f"✓ Sentiment data received")
        print(f"  Articles analyzed: {data.get('articles_analyzed', 0)}")
    else:
        print(f"✗ Status: {r.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 6: Portfolio (Protected)
print("\n[6] Testing Portfolio (Protected Endpoint)...")
try:
    r = requests.get(f'{BASE_URL}/portfolio', headers=headers, timeout=5)
    if r.status_code == 200:
        print(f"✓ Portfolio retrieved: {len(r.json())} items")
    elif r.status_code == 401:
        print(f"✗ Unauthorized (token may be invalid)")
    else:
        print(f"✗ Status: {r.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
