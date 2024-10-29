from flask import Flask, render_template, request, make_response
import sqlite3
import datetime

app = Flask(__name__)
DB_PATH = "counter.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS global_count (id INTEGER PRIMARY KEY, count INTEGER)"
    )
    cursor.execute("INSERT OR IGNORE INTO global_count (id, count) VALUES (1, 0)")
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS qr_counter (
            qr_id TEXT PRIMARY KEY,
            count INTEGER
        )
        """
    )
    conn.commit()
    conn.close()

def increment_global_counter():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cursor = conn.cursor()
    cursor.execute("BEGIN EXCLUSIVE")
    cursor.execute("UPDATE global_count SET count = count + 1 WHERE id = 1")
    conn.commit()
    cursor.execute("SELECT count FROM global_count WHERE id = 1")
    global_count = cursor.fetchone()[0]
    conn.close()
    return global_count

def increment_qr_counter(qr_id):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cursor = conn.cursor()
    cursor.execute("BEGIN EXCLUSIVE")
    
    cursor.execute("SELECT count FROM qr_counter WHERE qr_id = ?", (qr_id,))
    result = cursor.fetchone()
    
    if result:
        cursor.execute("UPDATE qr_counter SET count = count + 1 WHERE qr_id = ?", (qr_id,))
        qr_count = result[0] + 1
    else:
        cursor.execute("INSERT INTO qr_counter (qr_id, count) VALUES (?, 1)", (qr_id,))
        qr_count = 1

    conn.commit()
    conn.close()
    return qr_count

@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cursor = conn.cursor()
    qr_id = request.args.get("papere")
    visited = request.cookies.get(f"visited_{qr_id}")
    
    if visited:
        cursor.execute("SELECT count FROM global_count WHERE id = 1")
        global_count = cursor.fetchone()[0]
        
        if qr_id and qr_id != "":
            cursor.execute("SELECT count FROM qr_counter WHERE qr_id = ?", (qr_id,))
            qr_count = cursor.fetchone()[0]
        else:
            qr_count = 0

        conn.close()
    else:
        global_count = increment_global_counter()

        if qr_id and qr_id != "":
            qr_count = increment_qr_counter(qr_id)
            response = make_response(render_template("index.html", global_count=global_count, qr_count=qr_count))
        else:
            response = make_response(render_template("index.html", global_count=global_count, qr_count=0))

        expires = datetime.datetime.now() + datetime.timedelta(days=1)
        response.set_cookie(f"visited_{qr_id}", "yes", expires=expires)
        conn.close()
        return response

    return render_template("index.html", global_count=global_count, qr_count=qr_count)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
