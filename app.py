import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

from flask import Flask, jsonify, request
import recommendations
import requests

app = Flask(__name__)

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