import psycopg2
import time
from decouple import config


def get_connection():
    return psycopg2.connect(
        dbname=config('DB_NAME'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        host=config('DB_HOST'),
        port=config('DB_PORT')
    )


def init_db():
    for i in range(10):
        try:
            conn = get_connection()
            with conn.cursor() as cur:

                # Users table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id         SERIAL PRIMARY KEY,
                        name       VARCHAR(100) NOT NULL,
                        dob        DATE NOT NULL,
                        email      VARCHAR(150) NOT NULL UNIQUE,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)

                # Sales table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sales (
                        id       SERIAL PRIMARY KEY,
                        month    VARCHAR(20) NOT NULL,
                        amount   NUMERIC(10,2) NOT NULL,
                        category VARCHAR(50),
                        region   VARCHAR(50)
                    );
                """)

                # Seed dummy sales data if table is empty
                cur.execute("SELECT COUNT(*) FROM sales;")
                count = cur.fetchone()[0]
                if count == 0:
                    cur.execute("""
                        INSERT INTO sales (month, amount, category, region) VALUES
                        ('Jan', 85000,  'Electronics', 'North'),
                        ('Jan', 32000,  'Furniture',   'South'),
                        ('Feb', 62000,  'Electronics', 'East'),
                        ('Feb', 28000,  'Accessories', 'West'),
                        ('Mar', 91000,  'Electronics', 'North'),
                        ('Mar', 41000,  'Furniture',   'South'),
                        ('Apr', 74000,  'Electronics', 'East'),
                        ('Apr', 19000,  'Accessories', 'West'),
                        ('May', 95000,  'Electronics', 'North'),
                        ('May', 37000,  'Furniture',   'South'),
                        ('Jun', 88000,  'Electronics', 'East'),
                        ('Jun', 24000,  'Accessories', 'West');
                    """)
                    print("Sales dummy data inserted")

            conn.commit()
            conn.close()
            print("Database initialised successfully")
            return
        except psycopg2.OperationalError as e:
            print(f"DB not ready, retrying in 2s... ({i+1}/10)")
            time.sleep(2)
    raise Exception("Could not connect to database after 10 retries")
