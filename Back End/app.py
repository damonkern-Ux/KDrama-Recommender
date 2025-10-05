from flask import Flask, request, jsonify
from flask_cors import CORS
from trending_get import trending
from main_recommender import recommender

app = Flask(__name__)
CORS(app)

# Basic user. For testing purposes.
valid_user = {"username": "A", "password": "iamademon"}


# the trending info getter.
try:
    trending()
except Exception as e:
    trends = []
    print("Error fetching trends:", e)


# login route
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == valid_user["username"] and password == valid_user["password"]:
        return jsonify({"status": "ok", "message": "Login successful!"})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401


# trending route
@app.route("/trending", methods=["GET"])
def get_trending():
    if not trends:
        return (
            jsonify({"status": "fail", "message": "No internet or no trends found"}),
            500,
        )
    return jsonify({"status": "ok", "trending": trends})

# recommendations route
@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    try:
        recommendation = recommender()
        if not recommendation:
            return jsonify({"status": "fail", "message": "No recommendations available"}), 404
        return jsonify({"status": "ok", "recommendations": recommendation})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
