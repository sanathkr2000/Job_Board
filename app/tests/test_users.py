import pytest
from fastapi.testclient import TestClient
from app.main import app  # Adjust path if needed

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

# ✅ Positive Test Case
def test_get_users_valid(test_client):
    response = test_client.get("/users/fetch-all?page=1&page_size=100")
    assert response.status_code == 200
    json_response = response.json()
    assert "users" in json_response
    assert "total" in json_response
    assert isinstance(json_response["users"], list)

# ❌ Negative Test Case 1: Missing required query parameters (if required)
def test_get_users_missing_params(test_client):
    response = test_client.get("/users/fetch-all/")
    assert response.status_code in [422, 400], "Expected error status code for missing params"
    # Optionally check for validation error message
    # assert "detail" in response.json()


def test_fetch_jobs_with_filters(test_client):
    # Test with valid filters
    # response = test_client.get("/jobs/filter?skip=ABC&limit=ABC")
    response = test_client.get("/users/fetch-all?page=ABC&page_size=ABC")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Ensure it's a list of jobs
    assert len(data) <= 10  # Check that the number of jobs does not exceed the limit

def test_fetch_jobs_with_types(test_client):
    # Test with valid filters
    response = test_client.get("/users/fetch-all?page=ABC&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Ensure it's a list of jobs
    # assert len(data) <= 10  # Check that the number of jobs does not exceed the limit


def test_get_users_negative_page_values(test_client):
    # Test with valid filters
    response = test_client.get("/users/fetch-all?page=-1&page_size=-10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Ensure it's a list of jobs
    # assert len(data) <= 10  # Check that the number of jobs does not exceed the limit

# ❌ Negative Test Case 4: Excessive page size (if there's a limit)
def test_get_users_excessive_page_size(test_client):
    response = test_client.get("/users/fetch-all?page=1&page_size=10000")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Ensure it's a list of jobs
