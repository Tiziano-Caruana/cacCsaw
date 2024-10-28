from flask import Flask, render_template, request, make_response
import sqlite3
import datetime

app = Flask(__name__)
DB_PATH = "counter.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS visit_count (id INTEGER PRIMARY KEY, count INTEGER)"
    )
    cursor.execute("INSERT OR IGNORE INTO visit_count (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

def increment_counter():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cursor = conn.cursor()
    cursor.execute("BEGIN EXCLUSIVE")
    cursor.execute("UPDATE visit_count SET count = count + 1 WHERE id = 1")
    conn.commit()
    cursor.execute("SELECT count FROM visit_count WHERE id = 1")
    count = cursor.fetchone()[0]
    conn.close()
    return count

@app.route("/")
def index():
    visited = request.cookies.get("visited")
    if visited:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM visit_count WHERE id = 1")
        count = cursor.fetchone()[0]
        conn.close()
    else:
        count = increment_counter()
        
        response = make_response(render_template("index.html", count=count))
        expires = datetime.datetime.now() + datetime.timedelta(days=1)
        response.set_cookie("visited", "yes", expires=expires)
        return response

    return render_template("index.html", count=count)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=80)
