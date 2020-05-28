from database.conn import DatabaseConnection

with DatabaseConnection('./database/data.db') as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS items (store_name text, item text, price real)")  # be sure table exists
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)")