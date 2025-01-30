from fastapi import FastAPI
from pymongo import MongoClient
import urllib.parse
import os 
import pandas as pd
app = FastAPI()

# Your raw MongoDB password
raw_password = "aditya@2002"  # Replace with your actual password

# URL-encode the password
encoded_password = urllib.parse.quote_plus(raw_password)

# Corrected MongoDB URI
MONGO_URI = f"mongodb+srv://adjangam9:{encoded_password}@crud-api.wzzzdr2.mongodb.net/?retryWrites=true&w=majority&appName=CRUD-API"

client = MongoClient(MONGO_URI)
db = client["tree_management"]  # Database Name

# Define Collections
requests_collection = db["requests"]
work_orders_collection = db["work_orders"]

# CSV File Paths
REQUESTS_CSV = "fake_service_requests.csv"
WORK_ORDERS_CSV = "extended_work_orders.csv"

# Required column structure
REQUESTS_COLUMNS = ["Request ID", "Date", "Location", "Issue Type", "Priority", "Status", "Assigned To"]
WORK_ORDERS_COLUMNS = ["Work Order ID", "Tree ID", "Latitude", "Longitude", "Date Created", "Created By", 
                       "Creator ID", "Creator Role", "Assigned To", "Details", "Notes", "Status", 
                       "Priority", "Work Type", "Due Date", "Completion Date", "Materials Used", "Cost Estimate"]

# Function to load CSV into MongoDB
def load_csv_to_mongo(csv_file, collection, required_columns):
    if not os.path.exists(csv_file):
        print(f"File {csv_file} not found.")
        return {"error": f"CSV file {csv_file} not found"}

    df = pd.read_csv(csv_file)

    # Validate if CSV contains required columns
    if not all(col in df.columns for col in required_columns):
        print(f"CSV {csv_file} is missing required columns.")
        return {"error": f"CSV {csv_file} is missing required columns"}

    data = df.to_dict(orient="records")
    
    # Clear previous data (optional)
    collection.delete_many({})
    
    # Insert new data
    collection.insert_many(data)

    return {"message": f"Uploaded {len(data)} records from {csv_file} to MongoDB"}

# 🟢 API Route to Upload CSV Data to MongoDB
@app.post("/upload_csv/")
async def upload_csv_data():
    requests_result = load_csv_to_mongo(REQUESTS_CSV, requests_collection, REQUESTS_COLUMNS)
    work_orders_result = load_csv_to_mongo(WORK_ORDERS_CSV, work_orders_collection, WORK_ORDERS_COLUMNS)
    
    return {
        "requests_upload": requests_result,
        "work_orders_upload": work_orders_result
    }
