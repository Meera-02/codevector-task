from fastapi import FastAPI, Query
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")

@app.get("/products")
def get_products(
    category: str = None,
    cursor: int = None,
    limit: int = 10
):
    conn = get_connection()
    cur = conn.cursor()

    if category and cursor:
        cur.execute("""
            SELECT id, name, category, price, created_at
            FROM products
            WHERE category = %s AND id < %s
            ORDER BY id DESC
            LIMIT %s
        """, (category, cursor, limit))
    elif category:
        cur.execute("""
            SELECT id, name, category, price, created_at
            FROM products
            WHERE category = %s
            ORDER BY id DESC
            LIMIT %s
        """, (category, limit))
    elif cursor:
        cur.execute("""
            SELECT id, name, category, price, created_at
            FROM products
            WHERE id < %s
            ORDER BY id DESC
            LIMIT %s
        """, (cursor, limit))
    else:
        cur.execute("""
            SELECT id, name, category, price, created_at
            FROM products
            ORDER BY id DESC
            LIMIT %s
        """, (limit,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    products = [
        {"id": r[0], "name": r[1], "category": r[2], "price": r[3], "created_at": str(r[4])}
        for r in rows
    ]

    next_cursor = products[-1]["id"] if products else None

    return {"products": products, "next_cursor": next_cursor}
