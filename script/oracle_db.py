# scripts/oracle_db.py

import pandas as pd
import oracledb
import os

PROCESSED_DATA_PATH = "../data/processed/reviews_with_themes.csv"

# Replace with your actual Oracle connection info
ORACLE_USER = os.getenv("ORACLE_USER", "your_user")
ORACLE_PWD = os.getenv("ORACLE_PWD", "your_password")
ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost/XEPDB1")  # typical for Oracle XE

def connect_to_db():
    """
    Establish Oracle DB connection using environment variables.
    """
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
        print("[INFO] Connected to Oracle DB.")
        return conn
    except oracledb.Error as e:
        print(f"[ERROR] Could not connect to Oracle DB: {e}")
        raise

def create_tables(conn):
    """
    Create Banks and Reviews tables.
    """
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE banks (
                id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name VARCHAR2(100) UNIQUE NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE reviews (
                id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                bank_id NUMBER REFERENCES banks(id),
                review_text CLOB,
                rating NUMBER,
                review_date DATE,
                sentiment_label VARCHAR2(20),
                sentiment_score FLOAT,
                keywords CLOB,
                theme VARCHAR2(50),
                source VARCHAR2(50)
            )
        """)
        print("[INFO] Tables created successfully.")

def insert_data(conn, df):
    """
    Insert reviews and banks into database.
    """
    with conn.cursor() as cur:
        # Insert unique banks first
        bank_names = df['bank'].unique()
        for name in bank_names:
            cur.execute("MERGE INTO banks b USING (SELECT :1 AS name FROM dual) d ON (b.name = d.name) WHEN NOT MATCHED THEN INSERT (name) VALUES (d.name)", [name])
        
        # Insert reviews
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, keywords, theme, source)
                VALUES (
                    (SELECT id FROM banks WHERE name = :1),
                    :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, :7, :8, :9
                )
            """, [
                row['bank'], row['clean_review'], int(row['rating']), row['date'],
                row['sentiment_label'], float(row['sentiment_score']),
                row.get('keywords', ''), row.get('theme', ''), row.get('source', 'Google Play')
            ])
        conn.commit()
        print(f"[INFO] Inserted {len(df)} records into the database.")

def main():
    df = pd.read_csv(PROCESSED_DATA_PATH)
    conn = connect_to_db()
    try:
        create_tables(conn)
    except oracledb.Error as e:
        print(f"[WARNING] Tables may already exist: {e}")
    insert_data(conn, df)
    conn.close()

if __name__ == "__main__":
    main()
