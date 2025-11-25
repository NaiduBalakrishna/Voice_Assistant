from flask import Flask, request, jsonify, render_template, session
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
USERS_FILE = "users.json"


# ---------------- JSON LOAD/SAVE ----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({"users": []}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- PAGE ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    users = load_users()

    for user in users["users"]:
        if user["email"] == email:
            return jsonify({"error": "Email already exists!"}), 400

    users["users"].append({
        "username": username,
        "email": email,
        "password": password
    })
    save_users(users)

    return jsonify({"message": "registered"})


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    users = load_users()

    for user in users["users"]:
        if user["email"] == email and user["password"] == password:
            session["username"] = user["username"]

            # GREETING BASED ON TIME
            hour = datetime.now().hour
            if hour < 12:
                greeting = f"Good morning {user['username']}. How can I help you?"
            elif hour < 17:
                greeting = f"Good afternoon {user['username']}. How can I help you?"
            else:
                greeting = f"Good evening {user['username']}. How can I help you?"

            return jsonify({
                "message": "login_success",
                "username": user["username"],
                "greeting": greeting
            })

    return jsonify({"error": "Invalid email or password"}), 401


# ---------------- ASSISTANT LOGIC ----------------
@app.route("/process", methods=["POST"])
def process():
    data = request.json
    text = (data.get("text") or "").lower().strip()

    # Known commands
    if any(word in text for word in ["hi", "hello", "hey"]):
        return jsonify({"reply": "Hello Sir, How may I help you?"})

    if "who are you" in text or "your name" in text:
        return jsonify({"reply": "My name is JARVIS. I worked as a voice assistant for Ironman, and now I am happy to work with you."})

    if "open google" in text:
        return jsonify({"reply": "Opening Google...", "action": "open", "url": "https://www.google.com"})

    if "open youtube" in text:
        return jsonify({"reply": "Opening YouTube...", "action": "open", "url": "https://www.youtube.com"})

    if "open facebook" in text:
        return jsonify({"reply": "Opening Facebook...", "action": "open", "url": "https://facebook.com"})
    if "bye" in text:
        return jsonify({"reply": "bye sir have a nice day"})

    if "time" in text:
        now = datetime.now().strftime("%I:%M %p")
        return jsonify({"reply": f"The current time is {now}."})

    # Fallback (Google search)
    query = text.replace(" ", "+")
    google_url = f"https://www.google.com/search?q={query}"

    return jsonify({
        "reply": f"Searching Google for {text}",
        "action": "open",
        "url": google_url
    })


# ---------------- LOGOUT ----------------
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "logged_out"})


if __name__ == "__main__":
    app.run(debug=True)
