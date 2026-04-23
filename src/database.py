import sqlite3
import os
import json


class Database:
    def __init__(self, db_path="data/database.sqlite"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Products table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    niche_id TEXT NOT NULL,
                    source_url TEXT UNIQUE NOT NULL,
                    title TEXT,
                    price TEXT,
                    sales_30d INTEGER,
                    image_urls TEXT,
                    raw_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Contents table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    script TEXT,
                    video_path TEXT,
                    status TEXT DEFAULT 'PENDING',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """
            )

            # Post history table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS post_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_id INTEGER,
                    tiktok_url TEXT,
                    views INTEGER DEFAULT 0,
                    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (content_id) REFERENCES contents (id)
                )
            """
            )
            conn.commit()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def add_product(
        self,
        niche_id,
        source_url,
        title,
        price,
        sales_30d,
        image_urls,
        raw_data,
    ):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO products
                    (niche_id, source_url, title, price, sales_30d, image_urls, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        niche_id,
                        source_url,
                        title,
                        price,
                        sales_30d,
                        image_urls,
                        raw_data,
                    ),
                )
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # Already exists
                return None

    def add_content(self, product_id, script_data, status="PENDING"):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO contents (product_id, script, status)
                VALUES (?, ?, ?)
            """,
                (product_id, json.dumps(script_data), status),
            )
            conn.commit()
            return cursor.lastrowid

    def update_content_video_path(self, content_id, video_path):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE contents SET video_path = ?, status = 'READY'
                WHERE id = ?
            """,
                (video_path, content_id),
            )
            conn.commit()
