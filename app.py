from flask import Flask, jsonify, request

app = Flask(__name__)

PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": "Mon: 5x5 Back Squat + AMRAP\nTue: EMOM 20min Assault Bike\nWed: Bench Press + 21-15-9\nThu: 10RFT Deadlifts/Box Jumps\nFri: 30min Active Recovery",
        "diet": "B: 3 Egg Whites + Oats Idli\nL: Grilled Chicken + Brown Rice\nD: Fish Curry + Millet Roti\nTarget: 2,000 kcal",
        "color": "#e74c3c"
    },
    "Muscle Gain (MG)": {
        "workout": "Mon: Squat 5x5\nTue: Bench 5x5\nWed: Deadlift 4x6\nThu: Front Squat 4x8\nFri: Incline Press 4x10\nSat: Barbell Rows 4x10",
        "diet": "B: 4 Eggs + PB Oats\nL: Chicken Biryani (250g Chicken)\nD: Mutton Curry + Jeera Rice\nTarget: 3,200 kcal",
        "color": "#2ecc71"
    },
    "Beginner (BG)": {
        "workout": "Circuit Training: Air Squats, Ring Rows, Push-ups.\nFocus: Technique Mastery & Form (90% Threshold)",
        "diet": "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati.\nProtein: 120g/day",
        "color": "#3498db"
    }
}

# all-lowercase collection
PROGRAMS_LOWER = {k.lower(): v for k, v in PROGRAMS.items()}

@app.route("/api/v1.0", methods=["GET"])
def api_root():
    return jsonify({
        "version": "1.0",
        "status": "active",
        "available_endpoints": {
            "programs": "/api/v1.0/programs",
            "health": "/api/v1.0/health",
            "weekly_workout_chart": "/api/v1.0/weekly_workout_chart",
            "daily_nutrition_plan": "/api/v1.0/daily_nutrition_plan",
            "entire_plan": "/api/v1.0/entire_plan"
        }
    }), 200

@app.route("/api/v1.0/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "ACEest Fitness API V1.0 Backend"}), 200

@app.route("/api/v1.0/programs", methods=["GET"])
def get_all_programs():
    return jsonify({"programs": list(PROGRAMS.keys())}), 200

@app.route("/api/v1.0/weekly_workout_chart", methods=["GET"])
def get_weekly_workout_chart():
    program_name = request.args.get("program_name")
    if not program_name:
        return jsonify({"error": "Missing 'program_name' query parameter"}), 400

    program = PROGRAMS_LOWER.get(program_name.lower())
    if not program:
        return jsonify({"error": f"Program '{program_name}' not found"}), 404

    return jsonify({"weekly_workout_chart": program.get("workout")}), 200

@app.route("/api/v1.0/daily_nutrition_plan", methods=["GET"])
def get_daily_nutrition_plan():
    program_name = request.args.get("program_name")
    if not program_name:
        return jsonify({"error": "Missing 'program_name' query parameter"}), 400

    program = PROGRAMS_LOWER.get(program_name.lower())
    if not program:
        return jsonify({"error": f"Program '{program_name}' not found"}), 404

    return jsonify({"daily_nutrition_plan": program.get("diet")}), 200

@app.route("/api/v1.0/entire_plan", methods=["GET"])
def get_entire_plan():
    program_name = request.args.get("program_name")
    if not program_name:
        return jsonify({"error": "Missing 'program_name' query parameter"}), 400

    program = PROGRAMS_LOWER.get(program_name.lower())
    if not program:
        return jsonify({"error": f"Program '{program_name}' not found"}), 404

    return jsonify({
        "weekly_workout_chart": program.get("workout"),
        "daily_nutrition_plan": program.get("diet")
    }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
