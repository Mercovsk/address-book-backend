# Address Book API

An Address Book API that enables location-based contact discovery by searching nearby records using geographic coordinates. The API allows the user to store and manage address book entries with associated latitude and longitude data, then retrieve records within a specified latitude, longitude, distance_km parameters. 

## Tech Stack
- Python, FastAPI, Pydantic, SQLAlchemy, SQLModel, uvicorn

## Fields for Address Book
- Id
- Name
- Latitude
- Longitude

## Formulas
1. Bounding box algorithm
2. Haversine algorithm

## How To Run Locally

### Prerequisites
- Docker
- Python 3.11+

### 1. Clone the repo
git clone https://github.com/Mercovsk/address-book-backend
cd address-book-backend

### 2. Run the repository in Docker
docker compose up -d

### 3. Open the API Documentation
Visit: http://localhost:8000/docs