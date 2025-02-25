from flask import Flask, jsonify, request
import recommendations

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hell():
    return {"Hello": "Node"}


@app.route("/accept-resources", methods=["POST"])
def receive_resources():
    resource_data = request.get_json()
    user_collection_resources = resource_data.get("userResources", [])
    all_db_resources = resource_data.get("DBResources", [])    
    user_text_resources = transform_resources(user_collection_resources)
    db_text_resources = transform_resources(all_db_resources)
    # Get recommendations
    finalRecommendations = recommendations.get_recommendations(
        user_text_resources,
        db_text_resources,
        top_n=3,
        similarity_threshold=0.1
    )
    
    return jsonify({
        "recommendations": finalRecommendations,
        "count": len(finalRecommendations)
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

# receive data from node.js backend #
# process the data (remove stop words, lowercase, lemmatize) #
# use recommendations.py to get the vectors and calculate cosine similaritiy
# find if similar resoruces are there in the database
# return first N similar resources from database else query the external API
