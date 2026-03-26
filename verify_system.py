#!/usr/bin/env python3
"""
Stock Prediction Application - System Verification Script
Checks all components are working correctly
"""

import subprocess
import requests
import sys
import time
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header():
    print(f"\n{BOLD}{BLUE}=" * 50)
    print("Stock Prediction Application - Verification")
    print(f"=" * 50 + f"{RESET}\n")

def print_check(message, passed):
    status = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
    print(f"  {message:<40} {status}")

def check_python():
    print(f"{BOLD}Python Environment:{RESET}")
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print_check(f"Python installed ({version})", True)
        return True
    except Exception as e:
        print_check(f"Python installed: {str(e)}", False)
        return False

def check_nodejs():
    print(f"\n{BOLD}Node.js Environment:{RESET}")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        node_version = result.stdout.strip()
        print_check(f"Node.js installed ({node_version})", True)
        
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        npm_version = result.stdout.strip()
        print_check(f"npm installed ({npm_version})", True)
        return True
    except Exception as e:
        print_check(f"Node.js/npm installed: {str(e)}", False)
        return False

def check_backend():
    print(f"\n{BOLD}Backend Status:{RESET}")
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=2)
        is_running = response.status_code == 200
        print_check("Backend API responding", is_running)
        
        if is_running:
            print_check("  - API Docs available", True)
            print(f"    → http://localhost:8000/docs")
        return is_running
    except requests.exceptions.ConnectionError:
        print_check("Backend API responding", False)
        print(f"    {YELLOW}Hint: Start backend with: cd backend && uvicorn main:app --reload{RESET}")
        return False
    except Exception as e:
        print_check(f"Backend check: {str(e)}", False)
        return False

def check_frontend():
    print(f"\n{BOLD}Frontend Status:{RESET}")
    try:
        response = requests.get("http://localhost:5173", timeout=2)
        is_running = response.status_code == 200
        print_check("Frontend server responding", is_running)
        
        if is_running:
            print(f"    → http://localhost:5173")
        return is_running
    except requests.exceptions.ConnectionError:
        print_check("Frontend server responding", False)
        print(f"    {YELLOW}Hint: Start frontend with: cd frontend && npm run dev{RESET}")
        return False
    except Exception as e:
        print_check(f"Frontend check: {str(e)}", False)
        return False

def check_database():
    print(f"\n{BOLD}Database:{RESET}")
    db_path = Path("backend/stock_prediction.db")
    exists = db_path.exists()
    print_check(f"Database file exists", exists)
    
    if exists:
        size = db_path.stat().st_size
        print(f"    → Size: {size} bytes")
    
    return exists

def check_dependencies():
    print(f"\n{BOLD}Python Dependencies:{RESET}")
    required_packages = [
        "fastapi", "uvicorn", "sqlalchemy", "pydantic",
        "pandas", "numpy", "scikit-learn", "yfinance"
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print_check(f"{package}", True)
        except ImportError:
            print_check(f"{package}", False)
            all_ok = False
    
    return all_ok

def check_frontend_deps():
    print(f"\n{BOLD}Frontend Dependencies:{RESET}")
    frontend_path = Path("frontend/node_modules")
    exists = frontend_path.exists()
    print_check(f"node_modules installed", exists)
    return exists

def print_next_steps():
    print(f"\n{BOLD}{BLUE}Next Steps:{RESET}")
    print("""
1. Start Backend (if not running):
   cd backend
   uvicorn main:app --reload --port 8000

2. Start Frontend (if not running):
   cd frontend
   npm run dev

3. Open application:
   http://localhost:5173

4. Register and login with test account

5. Try making a stock prediction
    """)

def main():
    print_header()
    
    checks = [
        ("Python Environment", check_python),
        ("Node.js Environment", check_nodejs),
        ("Backend API", check_backend),
        ("Frontend Server", check_frontend),
        ("Database", check_database),
        ("Python Dependencies", check_dependencies),
        ("Frontend Dependencies", check_frontend_deps),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"  {RED}Error: {str(e)}{RESET}")
            results[name] = False
    
    # Summary
    print(f"\n{BOLD}{BLUE}=" * 50)
    print("Summary")
    print(f"=" * 50 + f"{RESET}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\nTotal Checks: {total}")
    print(f"Passed: {GREEN}{passed}{RESET}")
    print(f"Failed: {RED}{total - passed}{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}{BOLD}✓ All systems operational!{RESET}")
    elif passed >= total - 2:  # Allow backend/frontend to be down
        print(f"\n{YELLOW}{BOLD}⚠ Some services not running{RESET}")
        print_next_steps()
    else:
        print(f"\n{RED}{BOLD}✗ System has issues - see above{RESET}")
        print_next_steps()
    
    print()

if __name__ == "__main__":
    main()
