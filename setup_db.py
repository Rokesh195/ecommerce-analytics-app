# setup_db.py
import sqlite3
import pandas as pd

# Paths to your CSVs
csv_files = {
    "eligibility": "eligibility.csv",
    "ad_sales": "ad_sales.csv",
    "total_sales": "total_sales.csv"
}

con = sqlite3.connect('ecommerce.db')
for table, path in csv_files.items():
    df = pd.read_csv(path)
    df.to_sql(table, con, if_exists='replace', index=False)

con.close()
print("DB Setup Complete")
