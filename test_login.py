import requests
import json

# Test login with the first registered user
r = requests.post(
    'http://localhost:8000/api/auth/login?username=test_user_now&password=Test123',
    timeout=5
)
print(f'Login Status Code: {r.status_code}')
if r.status_code == 200:
    print('SUCCESS: Login worked!')
    result = r.json()
    token = result.get('access_token', 'N/A')
    print(f'Access Token obtained (first 50 chars): {token[:50]}...')
    print(f'Token Type: {result.get("token_type")}')
else:
    print(f'ERROR: {r.text}')
