from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]


def test_cities_in_region():
    response = client.get("/regions/Spain")
    assert response.status_code == 200
    assert response.json() == ["Seville"]


def test_unknown_region():
    response = client.get("/regions/Atlantis")
    assert response.status_code == 404
    assert response.json() == {"detail": "Region not found"}


def test_city_list_route_rejects_post():
    response = client.post("/regions/Spain")
    assert response.status_code == 405


def test_region_path_in_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/regions/{region}" in response.json()["paths"]


def test_monthly_average():
    response = client.get("/regions/Spain/Seville/January")
    assert response.status_code == 200
    assert response.json() == {"high": 61, "low": 41}