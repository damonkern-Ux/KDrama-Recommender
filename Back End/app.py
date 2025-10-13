from flask import Flask, request, jsonify
from flask_cors import CORS
from trending_get import trending
from main_recommender import recommender
import combined_functions
import os

app = Flask(__name__)
CORS(app)

os.system("open './UI/Sign/sign-in.html'")
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
    trend_list = []
    for t in trends:
        trend_list.append(
            {
                "title": t[0],
                "year": t[1],
                "episodes": t[2],
                "platform": str(
                    str(str(t[3]).replace('"', "")).replace("[", "")
                ).replace("]", ""),
                "description": t[4],
            }
        )
    return jsonify({"status": "ok", "trending": trend_list})


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
        recommendation_list = []
        for t in recommendation:
            recommendation_list.append(
                {
                    "title": t[0],
                    "year": t[1],
                    "episodes": t[2],
                    "platform": str(
                        str(str(t[3]).replace('"', "")).replace("[", "")
                    ).replace("]", ""),
                    "description": t[4],
                }
            )
        return jsonify({"status": "ok", "recommendations": recommendation_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# watch-list route
@app.route("/watchlist", methods=["GET"])
def get_watchlist():
    try:
        watchlist = combined_functions.watch_list()
        if not watchlist:
            return jsonify({"status": "fail", "message": "Nothing in Watch List"}), 404
        watch_list = []
        for t in watchlist:
            watch_list.append(
                {"title": t[0], "year": t[1], "episode": t[2], "description": t[3]}
            )
        return jsonify({"status": "ok", "watchlist": watch_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# watch-list route
@app.route("/watchlistexplore", methods=["GET"])
def get_watchlistexplore():
    try:
        watchlist = combined_functions.watch_listexplore()
        if not watchlist:
            return jsonify({"status": "fail", "message": "Nothing in Watch List"}), 404
        watch_list = []
        for t in watchlist:
            watch_list.append(
                {"title": t[0], "year": t[1], "episode": t[2], "description": t[3]}
            )
        return jsonify({"status": "ok", "watchlist": watch_list})
    except Exception as e:
        return (
            jsonify({"status": "error", "message": str(e) + "\nIMDB Not Available"}),
            500,
        )


# watched-list route
@app.route("/watchedlist", methods=["GET"])
def get_watchedlist():
    try:
        watchedlist = combined_functions.watched_list()
        if not watchedlist:
            return jsonify({"status": "fail", "message": "Nothing Watched"}), 404
        watched_list = []
        for t in watchedlist:
            watched_list.append(
                {"title": t[0], "year": t[1], "episode": t[2], "time": t[3]}
            )
        return jsonify({"status": "ok", "watched": watched_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# wish-list route
@app.route("/wishlist", methods=["GET"])
def get_wishlist():
    try:
        wishlist = combined_functions.wish_list()
        if wishlist == "IMDB not Available":
            return jsonify({"status": "fail", "message": "IMDB not Available"}), 404
        if not wishlist:
            return jsonify({"status": "fail", "message": "Nothing Wished"}), 404
        wish_list = []
        for t in wishlist:
            wish_list.append(
                {
                    "title": t[0],
                    "year": t[1],
                    "description": t[2] if t[2] != "null" else "Not Available In IMDB.",
                }
            )
        return jsonify({"status": "ok", "wish": wish_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# updater route
@app.route("/update", methods=["POST"])
def update_profile():
    data = request.json
    drama_name = data.get("drama_name")
    status = data.get("status")
    out = combined_functions.updater(drama_name, status)
    if out != "done":
        return jsonify({"status": "error", "message": str(out)}), 500
    else:
        return jsonify({"status": "ok", "watched": out})


# profile route
@app.route("/profile", methods=["GET"])
def send_profile():
    out = combined_functions.profile()
    if not out:
        return jsonify({"status": "error", "message": str(out)}), 500
    else:
        out_ = {"watch": out[0], "watched": out[1], "wish": out[2]}
        return jsonify({"status": "ok", "watched": out_})


@app.route("/update-drama", methods=["POST"])
def update_drama():
    data = request.get_json()
    title = data["title"]
    action = data["action"]
    combined_functions.database_updator(title, action)
    return {"status": "ok"}


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    return_list = []
    search_results = combined_functions.search(data["query"])
    for drama in search_results:
        return_list.append(
            {
                "title": drama[0],
                "year": drama[1],
                "episodes": drama[2],
                "platform": str(
                    str(str(drama[3]).replace('"', "")).replace("[", "")
                ).replace("]", ""),
                "description": drama[4],
            }
        )
    return jsonify({"status": "ok", "search": return_list})


if __name__ == "__main__":
    app.run(debug=True)
