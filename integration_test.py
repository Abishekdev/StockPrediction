#!/usr/bin/env python3
"""
Stock Prediction Application - Integration Test
Tests all major components working together
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{RESET}\n")

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ {msg}{RESET}")

def test_backend_health():
    """Test backend API is running"""
    print_header("Testing Backend Health")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print_success("Backend API is responding")
            print(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend (is it running on port 8000?)")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_frontend_health():
    """Test frontend is running"""
    print_header("Testing Frontend Health")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print_success("Frontend is responding")
            return True
        else:
            print_error(f"Frontend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to frontend (is it running on port 5173?)")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_api_documentation():
    """Test API docs are available"""
    print_header("Testing API Documentation")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_success("Swagger UI documentation available")
            print_info(f"Access at: {BASE_URL}/docs")
        
        response = requests.get(f"{BASE_URL}/redoc", timeout=5)
        if response.status_code == 200:
            print_success("ReDoc documentation available")
            print_info(f"Access at: {BASE_URL}/redoc")
            return True
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_user_registration():
    """Test user registration endpoint"""
    print_header("Testing User Registration")
    test_email = f"testuser_{int(time.time())}@example.com"
    
    payload = {
        "username": f"testuser_{int(time.time())}",
        "email": test_email,
        "password": "TestPassword123!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("User registration successful")
            print(f"  Username: {data.get('username')}")
            print(f"  Email: {data.get('email')}")
            print(f"  User ID: {data.get('id')}")
            
            # Save for next tests
            return {
                "username": payload["username"],
                "password": payload["password"],
                "user_id": data.get('id')
            }
        elif response.status_code == 400:
            print_info("User may already exist (this is normal for repeated tests)")
            return {
                "username": payload["username"],
                "password": payload["password"],
                "user_id": None
            }
        else:
            print_error(f"Registration failed: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_user_login(user_data):
    """Test user login endpoint"""
    print_header("Testing User Login")
    
    params = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            params=params,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print_success("User login successful")
            print(f"  Token: {token[:20]}...")
            return token
        else:
            print_error(f"Login failed: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_stock_data():
    """Test stock data endpoint"""
    print_header("Testing Stock Data Endpoint")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/stock/data/AAPL?days=5",
            timeout=10
        )
        
        if response.status_code == 200:
            print_success("Stock data retrieved successfully")
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print(f"  Ticker: AAPL")
                print(f"  Data points: {len(data)}")
                print(f"  Latest: {data[-1]}")
            return True
        else:
            print_error(f"Failed to get stock data: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_predictions(token):
    """Test prediction endpoint"""
    print_header("Testing Prediction Endpoint")
    
    if not token:
        print_info("Skipping prediction test (no auth token)")
        return False
    
    payload = {
        "ticker": "AAPL",
        "days_ahead": 5
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/predict",
            json=payload,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Prediction generated successfully")
            print(f"  Ticker: {data.get('ticker')}")
            print(f"  Predicted Price: ${data.get('predicted_price', 'N/A')}")
            print(f"  Prediction Window: {data.get('prediction_window')} days")
            return True
        else:
            print_error(f"Prediction failed: {response.status_code}")
            print(response.text[:200])
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_sentiment_analysis():
    """Test sentiment analysis endpoint"""
    print_header("Testing Sentiment Analysis")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/sentiment/AAPL",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Sentiment analysis retrieved")
            print(f"  Ticker: AAPL")
            print(f"  Sentiment Score: {data.get('sentiment_score', 'N/A')}")
            print(f"  Label: {data.get('sentiment_label', 'N/A')}")
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print(f"\n{BOLD}{BLUE}")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*10 + "Stock Prediction - Integration Tests" + " "*13 + "║")
    print("╚" + "═"*58 + "╝")
    print(f"{RESET}")
    
    results = {}
    
    # Backend health
    results['Backend Health'] = test_backend_health()
    
    # Frontend health
    results['Frontend Health'] = test_frontend_health()
    
    # API Documentation
    results['API Documentation'] = test_api_documentation()
    
    # Stock data (public endpoint)
    results['Stock Data'] = test_stock_data()
    
    # Sentiment analysis
    results['Sentiment Analysis'] = test_sentiment_analysis()
    
    # User registration
    user_data = test_user_registration()
    results['User Registration'] = user_data is not None
    
    # User login
    token = None
    if user_data:
        token = test_user_login(user_data)
        results['User Login'] = token is not None
    else:
        results['User Login'] = False
    
    # Predictions (requires auth)
    if token:
        results['Predictions'] = test_predictions(token)
    else:
        results['Predictions'] = False
    
    # Summary
    print_header("Test Summary")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"Total Tests: {total}")
    print(f"Passed: {GREEN}{passed}{RESET}")
    print(f"Failed: {RED}{failed}{RESET}")
    
    print(f"\n{BOLD}Test Details:{RESET}")
    for test_name, result in results.items():
        status = f"{GREEN}✓ PASS{RESET}" if result else f"{RED}✗ FAIL{RESET}"
        print(f"  {test_name:<30} {status}")
    
    print()
    
    if passed == total:
        print(f"{GREEN}{BOLD}✓ ALL TESTS PASSED!{RESET}")
        print(f"\n{BOLD}Application is fully operational!{RESET}")
        print(f"\nAccess the application at:")
        print(f"  {BLUE}Frontend: {FRONTEND_URL}{RESET}")
        print(f"  {BLUE}API Docs: {BASE_URL}/docs{RESET}")
    elif passed >= total - 2:
        print(f"{YELLOW}{BOLD}⚠ Most tests passed{RESET}")
        print(f"Application is mostly functional.")
    else:
        print(f"{RED}{BOLD}✗ Some tests failed{RESET}")
        print(f"Please check the errors above.")
    
    print()

if __name__ == "__main__":
    run_all_tests()
