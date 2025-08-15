# TweetPulse Pro - High-Performance Analytics API
# Optimized for speed and efficiency
# Updated: August 15, 2025

from flask import Flask, jsonify, request, Response
from pymongo import MongoClient
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Optimized MongoDB connection with connection pooling
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.environ.get('MONGO_DB', 'bigdata_project')
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION', 'tweets')

# Singleton MongoDB client for better performance
class MongoConnection:
    _client = None
    
    @classmethod
    def get_collection(cls):
        if cls._client is None:
            cls._client = MongoClient(MONGO_URI, maxPoolSize=50, connectTimeoutMS=3000)
        return cls._client[MONGO_DB][MONGO_COLLECTION]

collection = MongoConnection.get_collection()

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    """Fast tweet retrieval with pagination and projection"""
    try:
        limit = min(int(request.args.get('limit', 100)), 1000)  # Cap at 1000
        skip = int(request.args.get('skip', 0))
        
        # Use projection to only get required fields for better performance
        projection = {'tweet': 1, 'prediction': 1, 'created_at': 1, '_id': 0}
        
        tweets = list(collection.find({}, projection)
                     .sort('_id', -1)
                     .skip(skip)
                     .limit(limit))
        
        return jsonify({
            'data': tweets,
            'count': len(tweets),
            'has_more': len(tweets) == limit
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    pipeline = [
        {"$group": {"_id": "$prediction", "count": {"$sum": 1}}}
    ]
    stats = list(collection.aggregate(pipeline))
    return jsonify(stats)

DOCS_HTML = """
<!doctype html>
<html>
    <head>
        <meta charset="utf-8"/>
    <title>TweetPulse Pro API Docs</title>
        <link href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" rel="stylesheet">
    </head>
    <body>
        <div id="swagger"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.ui = SwaggerUIBundle({
                url: 'https://petstore.swagger.io/v2/swagger.json',
                dom_id: '#swagger'
            });
        </script>
    </body>
    </html>
"""

@app.route('/api/docs')
def api_docs():
        return Response(DOCS_HTML, mimetype='text/html')

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
