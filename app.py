from fastapi import FastAPI, HTTPException
import pandas as pd
import uvicorn

app = FastAPI()

# Load CSV from the same directory
CSV_FILE = "fake_service_requests.csv"  # Change this to your actual CSV file name
data_storage = None

def load_csv():
    """Load CSV data into memory."""
    global data_storage
    try:
        df = pd.read_csv(CSV_FILE)
        required_columns = ["Request ID", "Date", "Location", "Issue Type", "Priority", "Status", "Assigned To"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")
        data_storage = df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        data_storage = None

# Load CSV at startup
load_csv()

@app.get("/requests/")
async def get_requests():
    """Fetch all service requests."""
    if data_storage is None:
        raise HTTPException(status_code=404, detail="No data available. Check if the CSV file exists and is valid.")
    return {"data": data_storage}

