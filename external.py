import requests
from config import SEARCH_API_KEY
from config import SEARCH_ENGINE_ID


def google_search(query, num_results=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": SEARCH_API_KEY,  # API Key
        "cx": SEARCH_ENGINE_ID,  # Custom Search Engine ID
        "num": num_results,  # Number of results to fetch
        "lr": "lang_en",  # Language filter (optional)
    }
    try:
        # send the request
        response = requests.get(url, params=params)
        response.raise_for_status()

        # parse JSON response
        data = response.json()

        # extract relevant search results
        recommendations = []
        if "items" in data:
            for item in data["items"]:
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
