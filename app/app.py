from flask import Flask, request, redirect, url_for, render_template_string
import os
import mysql.connector
from mysql.connector import Error
import time

app = Flask(__name__)

# --------------------
# DB config (read from env, fallback to defaults)
# --------------------
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "flaskuser")
DB_PASS = os.getenv("DB_PASS", "flaskpass")
DB_NAME = os.getenv("DB_NAME", "guestbook")

# --------------------
# HTML templates
# --------------------
INDEX_HTML = """
<!doctype html>
<title>Guestbook</title>
<h1>Guestbook</h1>
<form action="{{ url_for('save') }}" method="post">
  Name: <input type="text" name="name" required><br><br>
  Message:<br>
  <textarea name="message" rows="4" cols="50" required></textarea><br><br>
  <button type="submit">Save</button>
</form>
<p><a href="{{ url_for('entries') }}">View entries</a></p>
"""

ENTRIES_HTML = """
<!doctype html>
<title>Entries</title>
<h1>Entries</h1>
{% if entries %}
  <ul>
  {% for e in entries %}
    <li><strong>{{ e.name }}</strong> — {{ e.message | e }}</li>
  {% endfor %}
  </ul>
{% else %}
  <p>No entries yet.</p>
{% endif %}
<p><a href="{{ url_for('index') }}">Back</a></p>
"""

# --------------------
# DB helper functions
# --------------------
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        auth_plugin='mysql_native_password'
    )

def init_db(retries=10, delay=3):
    """Try to create DB and table, retry if MySQL not ready"""
    for i in range(retries):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
            )
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            cur.close()
            conn.close()

            conn2 = get_connection()
            cur2 = conn2.cursor()
            cur2.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn2.commit()
            cur2.close()
            conn2.close()
            print("✅ DB initialized successfully")
            return
        except Error as e:
            print(f"DB init failed, retrying ({i+1}/{retries}):", e)
            time.sleep(delay)
    print("❌ DB init failed after retries")

# --------------------
# Flask routes
# --------------------
@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

@app.route("/save", methods=["POST"])
def save():
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()
    if not name or not message:
        return redirect(url_for("index"))
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO entries (name, message) VALUES (%s, %s)",
            (name, message.replace("\n", " "))
        )
        conn.commit()
        cur.close()
        conn.close()
    except Error as e:
        print("Insert error:", e)
    return redirect(url_for("entries"))

@app.route("/entries")
def entries():
    rows = []
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT name, message FROM entries ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Error as e:
        print("Select error:", e)
    return render_template_string(ENTRIES_HTML, entries=rows)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
