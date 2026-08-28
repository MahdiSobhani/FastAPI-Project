import sqlite3

DATABASE="tasks.db"

def get_db():
    connection=sqlite3.connect(DATABASE)
    connection.row_factory=sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()

def init_db():
    connection=sqlite3.connect(DATABASE)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL)""")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id))""")

    connection.commit()
    connection.close()