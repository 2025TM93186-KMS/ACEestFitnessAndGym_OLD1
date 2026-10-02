import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Eliminates Cross-Origin blocking parameters for client apps

PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": (
            "Mon: Back Squat 5x5 + Core\n"
            "Tue: EMOM 20min Assault Bike\n"
            "Wed: Bench Press + 21-15-9\n"
            "Thu: Deadlift + Box Jumps\n"
            "Fri: Zone 2 Cardio 30min"
        ),
        "diet": (
            "Breakfast: Egg Whites + Oats\n"
            "Lunch: Grilled Chicken + Brown Rice\n"
            "Dinner: Fish Curry + Millet Roti\n"
            "Target: ~2000 kcal"
        ),
        "color": "#e74c3c",
        "calorie_factor": 22
    },
    "Muscle Gain (MG)": {
        "workout": (
            "Mon: Squat 5x5\n"
            "Tue: Bench 5x5\n"
            "Wed: Deadlift 4x6\n"
            "Thu: Front Squat 4x8\n"
            "Fri: Incline Press 4x10\n"
            "Sat: Barbell Rows 4x10"
        ),
        "diet": (
            "Breakfast: Eggs + Peanut Butter Oats\n"
            "Lunch: Chicken Biryani\n"
            "Dinner: Mutton Curry + Rice\n"
            "Target: ~3200 kcal"
        ),
        "color": "#2ecc71",
        "calorie_factor": 35
    },
    "Beginner (BG)": {
        "workout": (
            "Full Body Circuit:\n"
            "- Air Squats\n"
            "- Ring Rows\n"
            "- Push-ups\n"
            "Focus: Technique & Consistency"
        ),
        "diet": (
            "Balanced Tamil Meals\n"
            "Idli / Dosa / Rice + Dal\n"
            "Protein Target: 120g/day"
        ),
        "color": "#3498db",
        "calorie_factor": 26
    }
}

PROGRAMS_LOWER = {k.lower(): v for k, v in PROGRAMS.items()}


def init_db():
    """Initializes the database table"""
    with sqlite3.connect('aceest_fitness.db', timeout=10) as conn:
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
        cursor.close()


# Initialize database on startup
init_db()


@app.route("/api/v1.1", methods=["GET"])
def api_root():
    return jsonify({
        "version": "1.1",
        "status": "active",
        "available_endpoints": {
            "programs": "/api/v1.1/programs",
            "health": "/api/v1.1/health",
            "weekly_workout_chart": "/api/v1.1/weekly_workout_chart",
            "daily_nutrition_plan": "/api/v1.1/daily_nutrition_plan",
            "entire_plan": "/api/v1.1/entire_plan",
            "save_client": "/api/v1.1/save_client"
        }
    }), 200


@app.route("/api/v1.1/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "ACEest Fitness API V1.1 Backend"}), 200


@app.route("/api/v1.1/programs", methods=["GET"])
def get_all_programs():
    return jsonify({"programs": list(PROGRAMS.keys())}), 200


@app.route("/api/v1.1/weekly_workout_chart", methods=["GET"])
def get_weekly_workout_chart():
    program_name = request.args.get("program_name")
    if not program_name:
        return jsonify({"error": "Missing 'program_name' query parameter"}), 400

    program = PROGRAMS_LOWER.get(program_name.lower())
    if not program:
        return jsonify({"error": f"Program '{program_name}' not found"}), 404

    return jsonify({"weekly_workout_chart": program.get("workout")}), 200


@app.route("/api/v1.1/daily_nutrition_plan", methods=["GET"])
def get_daily_nutrition_plan():
    program_name = request.args.get("program_name")
    if not program_name:
        return jsonify({"error": "Missing 'program_name' query parameter"}), 400

    program = PROGRAMS_LOWER.get(program_name.lower())
    if not program:
        return jsonify({"error": f"Program '{program_name}' not found"}), 404

    return jsonify({"daily_nutrition_plan": program.get("diet")}), 200


@app.route("/api/v1.1/entire_plan", methods=["GET"])
def get_entire_plan():
    program_name = request.args.get("program_name")
    weight = request.args.get("weight", type=float)

    if not program_name:
        return jsonify({"error": "Missing 'program_name' query parameter"}), 400

    program = PROGRAMS_LOWER.get(program_name.lower())
    if not program:
        return jsonify({"error": f"Program '{program_name}' not found"}), 404

    response_data = {
        "program_name": program_name,
        "ui_color": program.get("color"),
        "weekly_workout_chart": program.get("workout"),
        "daily_nutrition_plan": program.get("diet"),
        "estimated_calories": None
    }

    if weight and weight > 0:
        response_data["estimated_calories"] = int(weight * program.get("calorie_factor"))

    return jsonify(response_data), 200


@app.route("/api/v1.1/save_client", methods=["POST"])
def save_client():
    """
    Accepts client parameters via JSON body request payload and stores inside SQLite database.
    Example payload format: {"name": "John Doe", "age": 28, "weight": 82.5, "program": "Fat Loss (FL)", "target_adherence": 85}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body payload parameters"}), 400

    name = data.get("name", "").strip()
    program = data.get("program", "")

    if not name or not program:
        return jsonify({"error": "Fields 'name' and 'program' are required structural items"}), 400

    selected_program = PROGRAMS_LOWER.get(program.lower())
    if not selected_program:
        return jsonify({"error": f"Program '{program}' not recognized"}), 404

    age = data.get("age", 0)
    weight = data.get("weight", 0.0)
    height = data.get("height", 0.0)
    target_weight = data.get("target_weight", weight)
    target_adherence = data.get("target_adherence", 100)

    # Derive dynamic calorie factor calculation variables
    calories = int(weight * selected_program.get("calorie_factor")) if weight > 0 else 0

    try:
        with sqlite3.connect('aceest_fitness.db', timeout=10) as conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO clients (
                    name, age, height, weight, program, 
                    calories, target_weight, target_adherence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                name, age, height, weight, program,
                calories, target_weight, target_adherence
            ))
            cursor.close()

        return jsonify({
            "message": f"Client '{name}' successfully registered to the database module.",
            "client": {
                "id": cursor.lastrowid,
                "name": name,
                "program": program,
                "calculated_calories": calories
            }
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": f"A client profile named '{name}' already exists in our system records."}), 409
    except Exception as e:
        return jsonify({"error": f"Database exception error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
