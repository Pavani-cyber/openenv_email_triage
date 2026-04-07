# inference.py
import requests

BASE_URL = "http://localhost:7860"

r = requests.post(f"{BASE_URL}/reset")
print(r.json())
