import requests
import os
from dotenv import load_dotenv
load_dotenv()
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def google_search(query, num_results):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "num": num_results,
        "lr": "lang_en",
    }
    try:
        # send the request
        response = requests.get(url, params=params)
        response.raise_for_status()

        recommendedResources = response.json()

        # extract relevant search results
        recommendations = []
        if "items" in recommendedResources:
            for item in recommendedResources["items"]:
                recommendations.append(
                    {
                        "title": item.get("title", "No Title"),
                        "link": item.get("link", "")
                    }
                )

        return recommendations
    except requests.exceptions.RequestException as e:
        print(f"Google Search API Error: {e}")
        return []
