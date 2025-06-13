from flask import Flask, request, jsonify
import logging
import sys

app = Flask(__name__)

# set up logging
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        app.logger.info(f"Login success for user: {username}")
        return jsonify({"message": "Login successful"}), 200
    else:
        app.logger.warning(f"Login failed for user: {username}")
        return jsonify({"message": "Login failed"}), 401

@app.route("/")
def home():
    return "Flask app is running."

if __name__ == "__main__":
    app.run(debug=True)