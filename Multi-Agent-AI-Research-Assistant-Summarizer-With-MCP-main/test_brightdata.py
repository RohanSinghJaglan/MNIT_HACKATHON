import requests
from dotenv import load_dotenv
import os

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('BRIGHT_DATA_API_TOKEN')}",
    "Content-Type": "application/json"
}

data = {
    "zone": "web_unlocker1",
    "url": "https://geo.brdtest.com/welcome.txt?product=unlocker&method=api",
    "format": "raw"
}

try:
    response = requests.post(
        "https://api.brightdata.com/request",
        json=data,
        headers=headers
    )
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    
    if response.status_code == 200:
        print("\n✅ BrightData API is working!")
        print("Zone 'web_unlocker1' is valid")
    else:
        print("\n❌ Error with BrightData API")
        
except Exception as e:
    print(f"❌ Error: {e}")
