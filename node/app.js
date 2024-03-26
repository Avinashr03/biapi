const express = require('express');
const cors = require('cors');
const { MongoClient } = require('mongodb');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// MongoDB connection URI from environment variable
const MONGO_URI = process.env.MONGO;

// Create a new MongoClient
const client = new MongoClient(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true });

// Connect to MongoDB
let db;
client.connect()
    .then(() => {
        console.log("Connected to MongoDB");
        db = client.db('video_sales');
    })
    .catch(err => console.error("Error connecting to MongoDB:", err));

// Enable Cross-Origin Resource Sharing (CORS)
app.use(cors());

// Global variable to keep track of the API calls
let i = 1;

// Route to retrieve collection data
app.get('/collection_data', async (req, res) => {
    try {
        // Retrieve total count of documents in the collection
        const total_count = await db.collection('videogame_sales').estimatedDocumentCount();

        // Calculate range for retrieval based on the current value of i
        const chunk_size = 1000;
        const start_index = chunk_size * (i - 1);
        if(start_index + chunk_size > total_count) {
            i = 1;
        }

        const end_index = Math.min(chunk_size * i, total_count);

        // Retrieve data from the collection within the specified range
        const collection_data = await db.collection('videogame_sales').find({}, { projection: { _id: 0 } }).skip(start_index).limit(chunk_size).toArray();

        // Increment the global variable i for the next API call
        i++;

        // Send response with collection data
        res.json(collection_data);
    } catch (err) {
        console.error("Error fetching collection data:", err);
        res.status(500).send("Internal Server Error");
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
