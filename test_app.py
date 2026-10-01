import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_v1_1_root(client):
    response = client.get('/api/v1.1')
    assert response.status_code == 200
    assert response.json['version'] == "1.1"

def test_case_insensitive_workout_lookup(client):
    # Verifies lookups with mixed case names resolve cleanly
    response = client.get('/api/v1.1/weekly_workout_chart?program_name=faT lOss (Fl)')
    assert response.status_code == 200
    assert "Zone 2 Cardio" in response.json['weekly_workout_chart']

def test_entire_plan_without_weight(client):
    response = client.get('/api/v1.1/entire_plan?program_name=Muscle Gain (MG)')
    assert response.status_code == 200
    assert response.json['ui_color'] == "#2ecc71"
    assert response.json['estimated_calories'] is None

def test_entire_plan_with_dynamic_calories(client):
    # Validates arithmetic rule configuration: 80kg * 35 calorie_factor = 2800 kcal
    response = client.get('/api/v1.1/entire_plan?program_name=Muscle Gain (MG)&weight=80')
    assert response.status_code == 200
    assert response.json['estimated_calories'] == 2800

def test_missing_parameter_handling(client):
    response = client.get('/api/v1.1/daily_nutrition_plan')
    assert response.status_code == 400
    assert "Missing 'program_name'" in response.json['error']

def test_invalid_plan_not_found(client):
    response = client.get('/api/v1.1/entire_plan?program_name=Crossfit')
    assert response.status_code == 404
