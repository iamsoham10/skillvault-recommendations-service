import random
import re
import nltk
import external
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

wordnet = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    words = nltk.word_tokenize(text.lower()) # convert to lowercase and tokenize 
    words = [
        wordnet.lemmatize(word)  # lemmatize() is used to convert words to their base form
        for word in words 
        if word.isalpha() and word not in stop_words  # isalpha() is used to remove numbers and punctuations
    ]
    return ' '.join(words)

def get_recommendations(user_resources, db_resources, top_n, similarity_threshold):
    if not user_resources or not db_resources:
        return []
    
    # create a set of user resources for faster lookup
    user_resource_set = set(user_resources)
    
    # preprocess user and db resources
    processed_user_resources = [preprocess_text(text) for text in user_resources]
    processed_db_resources = [preprocess_text(text) for text in db_resources]
    
    # combine all texts for TF-IDF
    all_resources = processed_user_resources + processed_db_resources
    
    # create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_resources)
    
    # split into user and DB vectors
    user_vectors = tfidf_matrix[:len(processed_user_resources)]
    db_vectors = tfidf_matrix[len(processed_user_resources):]
    
    # calculate similarity
    similarity_matrix = cosine_similarity(user_vectors, db_vectors)

    recommendations = []
    
    # get top recommendations for each user resource
    for i, user_similarities in enumerate(similarity_matrix):
        # get indices of similar items above threshold
        relevant_indices = [
            idx for idx, score in enumerate(user_similarities) 
            if score >= similarity_threshold
        ]
        
        top_indices = sorted(
            relevant_indices,
            key=lambda idx: user_similarities[idx],
            reverse=True
        )[:top_n]
        
        # add recommendations
        for idx in top_indices:
            recommended_resource = db_resources[idx]
            if recommended_resource not in user_resource_set:
                recommendations.append({
                "user_resource": processed_user_resources[i],
                "recommended_resource": processed_db_resources[idx],
                "similarity_score": float(user_similarities[idx])
            })
    
    # sort by similarity score
    recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
    # if no TF-IDF recommendations use Google Search API
    if recommendations == []:
        search_query = random.choice(processed_user_resources)  # take random user resource as the search query
        no_of_results = 4
        customSearchData = external.google_search(search_query, no_of_results)
        recommendations.append(customSearchData)

    return recommendations

