import sqlite3

con = sqlite3.connect("ecommerce.db")

for table in ["total_sales", "ad_sales", "eligibility"]:
    print(f"\n--- {table} ---")
    cursor = con.execute(f"PRAGMA table_info({table});")
    for col in cursor.fetchall():
        print(col)

con.close()
