from flask import Flask, request, jsonify
import sqlite3, os
from datetime import datetime
from utils import sha256_of_file
from feature_extractor import analyze_video

app = Flask(__name__)
DB = "sports.db"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        activity TEXT,
        squat_count INTEGER,
        cheat_decision TEXT,
        flags TEXT,
        video_hash TEXT,
        created_at TEXT
    )""")
    conn.commit()
    conn.close()

@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No file"}), 400
    name = request.form.get("name", "Anonymous")
    file = request.files["video"]
    filename = file.filename
    # secure filename basic handling
    filename = filename.replace(" ", "_")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Analyze with AI
    result = analyze_video(filepath)
    video_hash = sha256_of_file(filepath)

    # Save to DB
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""INSERT INTO results (name, activity, squat_count, cheat_decision, flags, video_hash, created_at)
                 VALUES (?,?,?,?,?,?,?)""",
              (name, "Squat", result.get("count",0), result.get("decision","UNKNOWN"),
               ",".join(result.get("flags",[])), video_hash, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "result": result})

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT name, activity, squat_count, cheat_decision, flags, created_at FROM results ORDER BY squat_count DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {"name": r[0], "activity": r[1], "squat_count": r[2], "cheat_decision": r[3],
         "flags": r[4], "created_at": r[5]}
        for r in rows
    ])

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
