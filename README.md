# Project Overview
This project contains a data ingestion pipeline built with Docker, Flask, FastAPI, and PostgreSQL.

## Architecture
- **Mock Server (Flask on Port 5000)**: Serves customer data from a JSON file. Emulates a third-party standard REST api endpoint with pagination.
- **Pipeline Service (FastAPI on Port 8000)**: Provides an endpoint to trigger data ingestion from the Mock Server using `dlt` (data load tool) which handles data extractions, type inferences, schema evolutions, and upsert load logics. It then writes these to PostgreSQL. Also serves endpoints to query the ingested customer data.
- **Database (PostgreSQL on Port 5432)**: Stores the ingested customers.

## How to run
1. Make sure Docker and Docker Compose are installed.
2. Build and run the services:
   ```bash
   docker-compose up -d --build
   ```

## API Endpoints
### Mock Server:
- `GET http://localhost:5000/api/customers?page=1&limit=5`
- `GET http://localhost:5000/api/customers/{id}`
- `GET http://localhost:5000/api/health`

### Pipeline Service:
- `POST http://localhost:8000/api/ingest`
- `GET http://localhost:8000/api/customers?page=1&limit=5`
- `GET http://localhost:8000/api/customers/{id}`
