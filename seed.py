import psycopg2
import os
from dotenv import load_dotenv
import random

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
cur = conn.cursor()

categories = ["Electronics", "Clothing", "Books", "Food", "Toys", "Sports", "Beauty", "Home"]

print("Generating 200,000 products...")

# Much faster - single query using generate_series
cur.execute("""
    INSERT INTO products (name, category, price)
    SELECT 
        'Product ' || i,
        (ARRAY['Electronics','Clothing','Books','Food','Toys','Sports','Beauty','Home'])[floor(random()*8+1)],
        round((random() * 9990 + 10)::numeric, 2)
    FROM generate_series(1, 200000) AS i;
""")

conn.commit()
cur.close()
conn.close()

print("Done! 200,000 products inserted!")