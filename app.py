from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import urllib.parse
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# MongoDB Configuration
raw_password = "aditya@2002"  # Replace with your actual password
encoded_password = urllib.parse.quote_plus(raw_password)
MONGO_URI = f"mongodb+srv://adjangam9:{encoded_password}@crud-api.wzzzdr2.mongodb.net/?retryWrites=true&w=majority&appName=CRUD-API"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.get_database("tree_management")

# Collections
service_requests = db["requests"]
work_orders = db["work_orders"]

# Function to serialize MongoDB documents safely
def serialize_doc(doc):
    """Convert MongoDB document to JSON-compatible format"""
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    for key, value in doc.items():
        if isinstance(value, float) and np.isnan(value):  # Convert NaN to None
            doc[key] = None
    return doc

### 📌 CRUD for Service Requests ###
@app.get("/requests/")
async def get_requests(skip: int = 0, limit: int = 10):
    """Fetch all service requests with pagination."""
    data = list(service_requests.find().skip(skip).limit(limit))
    return {"data": [serialize_doc(doc) for doc in data]}

@app.post("/requests/")
async def create_request(request: dict):
    """Create a new service request."""
    result = service_requests.insert_one(request)
    return {"message": "Request created", "id": str(result.inserted_id)}

@app.get("/requests/{request_id}")
async def get_request_by_id(request_id: str):
    """Get a service request by Request ID (not _id)."""
    request = service_requests.find_one({"Request ID": request_id})
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return serialize_doc(request)

@app.get("/requests/tree/{tree_id}")
async def get_requests_by_tree_id(tree_id: str):
    """Get service requests associated with a specific tree ID."""
    requests = list(service_requests.find({"Tree ID": tree_id}))
    if not requests:
        raise HTTPException(status_code=404, detail="No requests found for this tree ID")
    return {"data": [serialize_doc(doc) for doc in requests]}

@app.put("/requests/{request_id}")
async def update_request(request_id: str, update_data: dict):
    """Update a service request by Request ID."""
    result = service_requests.update_one({"Request ID": request_id}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Request not found or no changes made")
    return {"message": "Request updated"}

@app.delete("/requests/{request_id}")
async def delete_request(request_id: str):
    """Delete a service request by Request ID."""
    result = service_requests.delete_one({"Request ID": request_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"message": "Request deleted"}

@app.get("/requests/count")
async def count_requests():
    """Get the total count of service requests."""
    count = service_requests.count_documents({})
    return {"count": count}

### 📌 CRUD for Work Orders ###
@app.get("/workorders/")
async def get_work_orders(skip: int = 0, limit: int = 10):
    """Fetch all work orders with pagination."""
    data = list(work_orders.find().skip(skip).limit(limit))
    return {"data": [serialize_doc(doc) for doc in data]}

@app.post("/workorders/")
async def create_work_order(order: dict):
    """Create a new work order."""
    result = work_orders.insert_one(order)
    return {"message": "Work order created", "id": str(result.inserted_id)}

@app.get("/workorders/{workorder_id}")
async def get_work_order_by_id(workorder_id: str):
    """Get a work order by Work Order ID (not _id)."""
    order = work_orders.find_one({"Work Order ID": workorder_id})
    if order is None:
        raise HTTPException(status_code=404, detail="Work order not found")
    return serialize_doc(order)

@app.get("/workorders/tree/{tree_id}")
async def get_work_orders_by_tree_id(tree_id: str):
    """Get work orders associated with a specific tree ID."""
    orders = list(work_orders.find({"Tree ID": tree_id}))
    if not orders:
        raise HTTPException(status_code=404, detail="No work orders found for this tree ID")
    return {"data": [serialize_doc(doc) for doc in orders]}

@app.put("/workorders/{workorder_id}")
async def update_work_order(workorder_id: str, update_data: dict):
    """Update a work order by Work Order ID."""
    result = work_orders.update_one({"Work Order ID": workorder_id}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Work order not found or no changes made")
    return {"message": "Work order updated"}

@app.delete("/workorders/{workorder_id}")
async def delete_work_order(workorder_id: str):
    """Delete a work order by Work Order ID."""
    result = work_orders.delete_one({"Work Order ID": workorder_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Work order not found")
    return {"message": "Work order deleted"}

@app.get("/workorders/count")
async def count_work_orders():
    """Get the total count of work orders."""
    count = work_orders.count_documents({})
    return {"count": count}
