from flask import Flask, request, jsonify
from flask_cors import CORS
from trending_get import trending
from main_recommender import recommender
import combined_functions

app = Flask(__name__)
CORS(app)


# login route
@app.route("/login", methods=["POST"])
def login():
    # Basic user. For testing purposes.
    valid_user = {"username": "A", "password": "iamademon"}
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
    # the trending info getter.
    try:
        trends = trending()
    except Exception as e:
        trends = []
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
            return (
                jsonify({"status": "fail", "message": "No recommendations available"}),
                404,
            )
        return jsonify({"status": "ok", "recommendations": recommendation})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# watch-list route
@app.route("/watchlist", methods=["GET"])
def get_watchlist():
    try:
        watchlist = combined_functions.watch_list()
        if not watchlist:
            return jsonify({"status": "fail", "message": "Nothing in Watch List"}), 404
        return jsonify({"status": "ok", "watchlist": watchlist})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# watched-list route
@app.route("/watchedlist", methods=["GET"])
def get_watchedlist():
    try:
        watchedlist = combined_functions.watched_list()
        if not watchedlist:
            return jsonify({"status": "fail", "message": "Nothing Watched"}), 404
        return jsonify({"status": "ok", "watched": watchedlist})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# wish-list route
@app.route("/wishlist", methods=["GET"])
def get_wishlist():
    try:
        wishlist = combined_functions.wish_list()
        if not wishlist:
            return jsonify({"status": "fail", "message": "Nothing Wished"}), 404
        return jsonify({"status": "ok", "watched": wishlist})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# updater route
@app.route("/profile", methods=["POST"])
def update_profile():
    data = request.json
    drama_name = data.get("drama_name")
    status = data.get("status")
    out = combined_functions.updater(drama_name, status)
    if out != "done":
        return jsonify({"status": "error", "message": str(out)}), 500
    else:
        return jsonify({"status": "ok", "watched": out})


if __name__ == "__main__":
    app.run(debug=True)
