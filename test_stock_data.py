import requests

r = requests.get('http://localhost:8000/api/stock/data/NIFTY?days=100', timeout=10)
print(f'Status: {r.status_code}')
if r.status_code == 200:
    data = r.json()
    print(f'Data received: {len(data.get("data", []))} records')
    if len(data.get("data", [])) > 0:
        print(f'First record: {data["data"][0]}')
else:
    print(f'Error: {r.text}')
