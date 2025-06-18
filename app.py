import os
import nltk

# Define a consistent NLTK data directory
NLTK_DATA_PATH = os.path.join(os.getcwd(), 'nltk_data')
os.makedirs(NLTK_DATA_PATH, exist_ok=True)
nltk.data.path.append(NLTK_DATA_PATH)

# Download necessary corpora into that directory
try:
    nltk.download('punkt_tab', download_dir=NLTK_DATA_PATH)
except:
    nltk.download('punkt', download_dir=NLTK_DATA_PATH)
    
nltk.download('stopwords', download_dir=NLTK_DATA_PATH)
nltk.download('wordnet', download_dir=NLTK_DATA_PATH)
nltk.download('omw-1.4', download_dir=NLTK_DATA_PATH)
from flask import Flask, jsonify, request
import recommendations
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Hello, World!"

@app.route("/accept-resources", methods=["POST"])
def receive_resources():
    resource_data = request.get_json()
    user_collection_resources = resource_data.get("userResources", [])
    all_db_resources = resource_data.get("DBResources", [])
    user_text_resources = transform_resources(user_collection_resources)
    db_text_resources = transform_resources(all_db_resources)
    # get recommendations
    finalRecommendations = recommendations.get_recommendations(
        user_text_resources,
        db_text_resources,
        top_n=3,
        similarity_threshold=0.3
    )
    return jsonify({
        "recommendations": finalRecommendations
    })

def transform_resources(resources):
    transformed_resources = []
    for res in resources:
        # combine title, description and tags
        combined_text = f"{res.get('title', '').strip()} {res.get('description', '').strip()} {' '.join(res.get('tags', [])).strip()}"
        transformed_resources.append(combined_text)
    return transformed_resources


if __name__ == "__main__":
    app.run(debug=True)