import sqlite3

DB_PATH = "counter.db"

def dump_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Dump della tabella 'global_count':")
    cursor.execute("SELECT * FROM global_count")
    global_count_data = cursor.fetchall()
    for row in global_count_data:
        print(row)

    print("\nDump della tabella 'qr_counter':")
    cursor.execute("SELECT * FROM qr_counter")
    qr_counter_data = cursor.fetchall()
    for row in qr_counter_data:
        print(row)

    print("\nDump della tabella 'visit_log':")
    cursor.execute("SELECT * FROM visit_log")
    visit_log_data = cursor.fetchall()
    for row in visit_log_data:
        print(row)

    conn.close()

if __name__ == "__main__":
    dump_database()
