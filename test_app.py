import pytest
import sqlite3
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_test_db():
    conn = sqlite3.connect('aceest_fitness.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            age INTEGER,
            height REAL,
            weight REAL,
            program TEXT,
            calories INTEGER,
            target_weight REAL,
            target_adherence INTEGER
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    yield

def test_api_v1_1_root(client):
    response = client.get('/api/v1.1')
    assert response.status_code == 200
    assert response.json['version'] == "1.1"

def test_case_insensitive_workout_lookup(client):
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
