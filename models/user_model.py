from db import get_connection


def get_all_users():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, dob, email FROM users ORDER BY id DESC;")
            rows = cur.fetchall()
        return [
            {'id': r[0], 'name': r[1], 'dob': r[2], 'email': r[3]}
            for r in rows
        ]
    finally:
        conn.close()


def create_user(name, dob, email):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, dob, email) VALUES (%s, %s, %s);",
                (name, dob, email)
            )
        conn.commit()
    finally:
        conn.close()


def delete_user(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
    finally:
        conn.close()
