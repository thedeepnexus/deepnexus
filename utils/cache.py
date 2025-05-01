import sqlite3
import os

DB_PATH = os.path.abspath("data/index/cache_db.sqlite")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# DB 초기화
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            top_k INTEGER,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(query, top_k)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 캐시 조회
def get_cached_response(query, top_k=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT response FROM cache WHERE query = ? AND top_k = ?", (query, top_k))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# 캐시 저장
def cache_response(query, top_k, response):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO cache (query, top_k, response) VALUES (?, ?, ?)",
        (query, top_k, response)
    )
    conn.commit()
    conn.close()
