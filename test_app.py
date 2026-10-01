import pytest
from app import app

@pytest.fixture
def client():
    """Configures the isolated target runtime client test harness wrapper."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_root(client):
    """Validates metadata structures routing references."""
    response = client.get('/api/v1.0')
    assert response.status_code == 200
    assert "available_endpoints" in response.json

def test_health_check(client):
    response = client.get('/api/v1.0/health')
    assert response.status_code == 200
    assert response.json['status'] == "healthy"

def test_get_all_programs(client):
    response = client.get('/api/v1.0/programs')
    assert response.status_code == 200
    assert "Fat Loss (FL)" in response.json['programs']

def test_case_insensitive_workout_lookup(client):
    response = client.get('/api/v1.0/weekly_workout_chart?program_name=fat loss (fl)')
    assert response.status_code == 200
    assert "Back Squat" in response.json['weekly_workout_chart']

def test_case_insensitive_nutrition_lookup(client):
    response = client.get('/api/v1.0/daily_nutrition_plan?program_name=mUsCLe GaIn (Mg)')
    assert response.status_code == 200
    assert "3,200 kcal" in response.json['daily_nutrition_plan']

def test_entire_plan_lookup(client):
    response = client.get('/api/v1.0/entire_plan?program_name=Beginner (BG)')
    assert response.status_code == 200
    assert "weekly_workout_chart" in response.json
    assert "daily_nutrition_plan" in response.json

def test_missing_parameter_throws_400(client):
    response = client.get('/api/v1.0/entire_plan')
    assert response.status_code == 400
    assert "Missing 'program_name'" in response.json['error']

def test_invalid_program_throws_404(client):
    response = client.get('/api/v1.0/entire_plan?program_name=NonExistentPlan')
    assert response.status_code == 404
    assert "not found" in response.json['error']
