import aiosqlite
import os

DB_PATH = os.path.abspath("data/index/cache_db.sqlite")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# 비동기 DB 초기화
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                top_k INTEGER,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(query, top_k)
            )
        ''')
        await db.commit()

# 캐시 조회
async def get_cached_response(query: str, top_k: int = 5) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT response FROM cache WHERE query = ? AND top_k = ?", (query, top_k)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

# 캐시 저장
async def async_cache_response(query: str, top_k: int, response: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO cache (query, top_k, response) VALUES (?, ?, ?)",
            (query, top_k, response)
        )
        await db.commit()
