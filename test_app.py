import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/api/v1.0/health')
    assert response.status_code == 200
    assert response.json['status'] == "healthy"

def test_get_all_programs(client):
    response = client.get('/api/v1.0/programs')
    assert response.status_code == 200
    assert "Fat Loss (FL)" in response.json['programs']

def test_get_nutrition_success(client):
    response = client.get('/api/v1.0/daily_nutrition_plan?program_name=Muscle Gain (MG)')
    assert response.status_code == 200
    assert "3,200 kcal" in response.json['daily_nutrition_plan']

def test_get_nutrition_missing_param(client):
    response = client.get('/api/v1.0/daily_nutrition_plan')
    assert response.status_code == 400
    assert "Missing 'program_name'" in response.json['error']

def test_get_nutrition_not_found(client):
    response = client.get('/api/v1.0/daily_nutrition_plan?program_name=InvalidPlan')
    assert response.status_code == 404
