from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models.customer import Customer
from services.ingestion import ingest_data
import uvicorn

app = FastAPI()

# Create tables matching the model strictly on startup
Base.metadata.create_all(bind=engine)

@app.post("/api/ingest")
def trigger_ingestion():
    try:
        records_processed = ingest_data()
        return {"status": "success", "records_processed": records_processed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
def get_customers(page: int = Query(1, ge=1), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    customers = db.query(Customer).offset(skip).limit(limit).all()
    total = db.query(Customer).count()
    return {
        "data": customers,
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
