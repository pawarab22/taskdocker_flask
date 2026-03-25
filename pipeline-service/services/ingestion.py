import os
import requests
import dlt
from dlt.destinations import postgres
from datetime import datetime

def ingest_data():
    base_url = "http://mock-server:5000/api/customers"
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/customer_db")
    total_fetched = 0
    
    @dlt.resource(name="customers", write_disposition="merge", primary_key="customer_id", columns={"date_of_birth": {"data_type": "date"}, "created_at": {"data_type": "timestamp", "timezone": False}, "account_balance": {"data_type": "decimal"}})
    def fetch_flask_data():
        nonlocal total_fetched
        page = 1
        limit = 100
        while True:
            response = requests.get(base_url, params={"page": page, "limit": limit})
            response.raise_for_status()
            data = response.json()
            
            records = data.get("data", [])
            if not records:
                break
                
            for r in records:
                if r.get("date_of_birth"):
                    r["date_of_birth"] = datetime.strptime(r["date_of_birth"], "%Y-%m-%d").date()
                if r.get("created_at"):
                    r["created_at"] = datetime.strptime(r["created_at"], "%Y-%m-%dT%H:%M:%SZ")

            yield records
            total_fetched += len(records)
            
            if len(records) < limit:
                break
            page += 1

    pipeline = dlt.pipeline(
        pipeline_name='mock_server_pipeline',
        destination=postgres(credentials=db_url),
        dataset_name='public'
    )
    
    pipeline.run(fetch_flask_data)
    
    return total_fetched
