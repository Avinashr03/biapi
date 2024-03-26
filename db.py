import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://shriram_r__:password1234@cluster0.e4gsd9p.mongodb.net')
db = client['video_sales']  # Replace 'Avinash' with your database name

# Define collection name
collection_name = 'videogame_sales'

# Check if the collection already exists
if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)

# Read data from Excel file
excel_file = "C:\\8th semester\\BI lab\\videogame_sales.xlsx"  # Replace with the correct file path
data = pd.read_excel(excel_file)

# Insert data into MongoDB collection
db[collection_name].insert_many(data.to_dict(orient='records'))

# Print the first 5 rows to the console
print(data.head(5))

# Close MongoDB connection
client.close()
