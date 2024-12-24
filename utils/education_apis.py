import requests
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
API_NINJA_KEY = os.getenv('API_NINJA_KEY')
SCIENCE_FACT_KEY = os.getenv('SCIENTIFIC-FACTS-KEY')

def fetch_random_fact():
    api_url = "https://api.api-ninjas.com/v1/facts"
    api_key = API_NINJA_KEY  # Replace with your actual API key
    headers = {"X-Api-Key": api_key}

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data[0]["fact"] if data else "No facts found."
    else:
        return f"Error: {response.status_code} - {response.text}"

def fetch_celestial_body(body_name):
    api_url = f"https://api.le-systeme-solaire.net/rest/bodies/{body_name.lower()}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if "name" in data:
                return {
                    "name": data.get("englishName", "Unknown"),
                    "mass": f"{data.get('mass', {}).get('massValue', 'N/A')} × 10^{data.get('mass', {}).get('massExponent', '')} kg",
                    "gravity": f"{data.get('gravity', 'N/A')} m/s²",
                    "radius": f"{data.get('meanRadius', 'N/A')} km",
                    "moons": [moon["moon"] for moon in data.get("moons", []) if moon] if data.get("moons") else ["None"],
                    "orbit": f"{data.get('sideralOrbit', 'N/A')} Earth days"
                }
            else:
                return {"error": "No details found for this celestial body."}
        else:
            return {"error": f"API returned {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

import requests

def fetch_country(country):
    api_url = f"https://restcountries.com/v3.1/name/{country}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Handle currencies
                currencies = ", ".join(
                    [f"{value.get('name', 'Unknown')} ({value.get('symbol', '')})"
                     for key, value in data[0].get("currencies", {}).items()]
                )

                # Handle languages
                languages = ", ".join(data[0].get("languages", {}).values())

                # Handle capital
                capital = data[0].get("capital", [])
                capital = ", ".join(capital) if capital else "Unknown"

                # Handle flag
                flag_url = data[0].get("flags", {}).get("png", "")
                flag_url = flag_url if flag_url else "https://via.placeholder.com/150?text=No+Image"

                # Return structured data
                return {
                    "name": {
                        "common": data[0].get("name", {}).get("common", "Unknown"),
                        "official": data[0].get("name", {}).get("official", "Unknown")
                    },
                    "capital": capital,
                    "population": data[0].get("population", "Unknown"),
                    "area": data[0].get("area", "Unknown"),
                    "currency": currencies if currencies else "Unknown",
                    "language": languages if languages else "Unknown",
                    "flag": flag_url
                }
            else:
                return {"error": "No details found for this country."}
        else:
            return {"error": f"API returned {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}
