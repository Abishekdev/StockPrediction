import requests

# Final system verification
print("FINAL APPLICATION VERIFICATION")
print("=" * 50)

endpoints = [
    ("Health", "http://localhost:8000/api/health"),
    ("Stock Data", "http://localhost:8000/api/stock/data/AAPL?days=10"),
]

all_ok = True
for name, url in endpoints:
    try:
        r = requests.get(url, timeout=5)
        status = "OK" if r.status_code == 200 else f"Error {r.status_code}"
        print(f"✓ {name:15} {status}")
    except Exception as e:
        print(f"✗ {name:15} FAILED: {str(e)[:40]}")
        all_ok = False

print("=" * 50)
if all_ok:
    print("✓ ALL SYSTEMS OPERATIONAL")
else:
    print("✗ Some systems need attention")
