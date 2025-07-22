import sqlite3

DB_PATH = "ecommerce.db"

def run_query(sql_query):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(sql_query)
    cols = [col[0] for col in cur.description]
    rows = cur.fetchall()
    con.close()
    return cols, rows
