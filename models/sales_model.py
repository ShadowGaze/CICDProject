from db import get_connection

# Bar chart — total sales amount per month


def get_sales_by_month():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT month, SUM(amount)
                FROM sales
                GROUP BY month
                ORDER BY MIN(id);
            """)
            rows = cur.fetchall()
        return {
            'labels': [r[0] for r in rows],
            'values': [float(r[1]) for r in rows]
        }
    finally:
        conn.close()

# Pie chart — total sales amount per category


def get_sales_by_category():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT category, SUM(amount)
                FROM sales
                GROUP BY category
                ORDER BY SUM(amount) DESC;
            """)
            rows = cur.fetchall()
        return {
            'labels': [r[0] for r in rows],
            'values': [float(r[1]) for r in rows]
        }
    finally:
        conn.close()

# Line chart — total sales amount per month (same data, different chart)


def get_sales_trend():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT month, SUM(amount)
                FROM sales
                GROUP BY month
                ORDER BY MIN(id);
            """)
            rows = cur.fetchall()
        return {
            'labels': [r[0] for r in rows],
            'values': [float(r[1]) for r in rows]
        }
    finally:
        conn.close()

# Doughnut chart — sales split by region


def get_sales_by_region():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT region, SUM(amount)
                FROM sales
                GROUP BY region
                ORDER BY SUM(amount) DESC;
            """)
            rows = cur.fetchall()
        return {
            'labels': [r[0] for r in rows],
            'values': [float(r[1]) for r in rows]
        }
    finally:
        conn.close()
