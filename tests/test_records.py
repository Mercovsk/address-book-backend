from utils.geo import get_bounding_box, is_within_radius
from models import Record

# Unit Test: Test is_within_radius()

def test_geospatial_radius_calculation():
    lat1, lon1 = 14.4500, 120.9500
    lat2, lon2 = 14.4510, 120.9510

    assert is_within_radius(lat1, lon1, lat2, lon2, max_distance_km=1.0) is True
    assert is_within_radius(lat1, lon1, lat2, lon2, max_distance_km=0.05) is False

# Integration Test: Creating a Record

def test_create_record_endpoint(client):
    payload = {
        "name": "University of Perpetual Help System DALTA, Las Pinas Campus",
        "latitude": "14.451218",
        "longitude": "120.985430"
    }

    response = client.post("/records/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "University of Perpetual Help System DALTA, Las Pinas Campus"
    assert "id" in data

# End-to-End Test: Create Records and Use Search Nearby Records (Bounding Box & Haversine Algorithm)

def test_find_nearby_records(client, session):
    # Seeding: directly insert mock data into the temporary database
    close_record = Record(name="SM City Bacoor", latitude="14.446342", longitude="120.951033")
    far_record = Record(name="Nuvali", latitude="14.239423", longitude="121.057415")

    session.add(close_record)
    session.add(far_record)
    session.commit()

    response = client.get("/records/search?latitude=14.459922&longitude=120.960737&distance_km=3")

    assert response.status_code == 200
    results = response.json()

    assert len(results) == 1
    assert results[0]["name"] == "SM City Bacoor"
    