import sqlite3

def init_db():
    conn = sqlite3.connect("chat.db")

    with open("database/init.sql", "r") as f:
        sql_script = f.read()
        conn.executescript(sql_script)

    conn.close()
    print("✅ Database + Tables Created Successfully!")

if __name__ == "__main__":
    init_db()