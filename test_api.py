import requests
import json

print("Testing registration endpoint...")
try:
    r = requests.post(
        'http://localhost:8000/api/auth/register',
        json={
            'username': 'test_user_now',
            'email': 'test_now@example.com',
            'password': 'Test123'  # Shorter password within 72 bytes
        },
        timeout=5
    )
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")
    
    if r.status_code == 200:
        print("\n✓ Registration SUCCESSFUL!")
        print(json.dumps(r.json(), indent=2))
    else:
        print(f"\n✗ Error: {r.status_code}")
        
except Exception as e:
    print(f"Connection Error: {e}")
