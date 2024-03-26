from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

MONGO = os.getenv('MONGO')

# Connect to MongoDB
client = MongoClient(MONGO)
db = client['video_sales']
collection_name = 'videogame_sales'  # Replace 'your_collection_name' with the name of your collection

app = Flask(__name__)

CORS(app)


i = 1

@app.route('/collection_data', methods=['GET'])
def get_collection_data():
    global i
    
    # Retrieve total count of documents in the collection
    total_count = db[collection_name].count_documents({})
    
    # Calculate range for retrieval based on the current value of i
    chunk_size = total_count // (i % 10)
    start_index = chunk_size * (i - 1)
    end_index = min(chunk_size * i, total_count)
    
    # Retrieve data from the collection within the specified range, excluding the _id field
    collection_data = list(db[collection_name].find({}, {'_id': 0}).skip(start_index).limit(end_index - start_index))
    
    # Increment the global variable i for the next API call
    i += 1
    
    return jsonify(collection_data)


if __name__ == '__main__':
    app.run(debug=True)
