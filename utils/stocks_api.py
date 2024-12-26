import requests
from dotenv import load_dotenv
import os

def dividends(symbol):
    load_dotenv()
    api_key = os.getenv('POLYGON_KEY')
    api_url = f"https://api.polygon.io/v3/reference/dividends?ticker={symbol}&limit=1&apiKey={api_key}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data and 'results' in data and len(data['results']) > 0:
            return data['results'][0]
        else:
            return None
    else:
        return None
