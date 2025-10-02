from flask import Flask, request, jsonify
from flask_cors import CORS
from trending_get import trending
app = Flask(__name__)
CORS(app)

# Basic user. For testing purposes.
valid_user = {
    'username' : 'A',
    'password' : 'iamademon'
}
# the trending info getter.
trends = trending()
if len(trends)==0:
    # pass info to client side with proper message.
    print('No Internet')

@app.route("/login", methods = ["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == valid_user["username"] and password == valid_user["password"]:
        return jsonify({"status": "ok", "message": "Login successful!"})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)