from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Eliminates Cross-Origin blocking parameters for client apps

PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": "Mon: Back Squat 5x5 + Core\nTue: EMOM 20min Assault Bike\nWed: Bench Press + 21-15-9\nThu: Deadlift + Box Jumps\nFri: Zone 2 Cardio 30min",
        "diet": "Breakfast: Egg Whites + Oats\nLunch: Grilled Chicken + Brown Rice\nDinner: Fish Curry + Millet Roti\nTarget: ~2000 kcal",
        "color": "#e74c3c",
        "calorie_factor": 22
    },
    "Muscle Gain (MG)": {
        "workout": "Mon: Squat 5x5\nTue: Bench 5x5\nWed: Deadlift 4x6\nThu: Front Squat 4x8\nFri: Incline Press 4x10\nSat: Barbell Rows 4x10",
        "diet": "Breakfast: Eggs + Peanut Butter Oats\nLunch: Chicken Biryani\nDinner: Mutton Curry + Rice\nTarget: ~3200 kcal",
        "color": "#2ecc71",
        "calorie_factor": 35
    },
    "Beginner (BG)": {
        "workout": "Full Body Circuit:\n- Air Squats\n- Ring Rows\n- Push-ups\nFocus: Technique & Consistency",
        "diet": "Balanced Tamil Meals\nIdli / Dosa / Rice + Dal\nProtein Target: 120g/day",
        "color": "#3498db",
        "calorie_factor": 26
    }
}

PROGRAMS_LOWER = {k.lower(): v for k, v in PROGRAMS.items()}

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
            "entire_plan": "/api/v1.1/entire_plan"
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
    """
    Returns full program parameters.
    Calculates active macro targets if an optional weight query argument is provided.
    """
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
