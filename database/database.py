import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS reviews (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        phone_number TEXT,
                        visit_date TEXT,
                        food_rating INTEGER,
                        cleanliness_rating TEXT,
                        extra_comments TEXT,
                        total_rating INTEGER
                    )
                """
            )
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS reg_users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        age INTEGER,
                        phone_number TEXT,
                        city TEXT
                    )
                """
            )
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS dish_categories(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE
                    )
                """
            )
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS dishes(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        price INTEGER,
                        category_id INTEGER,
                        FOREIGN KEY (category_id) REFERENCES dish_categories (id)
                    )
                """
            )
        
        conn.commit()

    def execute(self, query: str, params: tuple):
        with sqlite3.connect(self.path) as conn:
            conn.execute(query, params)
            conn.commit()

    def fetch(self, query: str, params: tuple = None):
        with sqlite3.connect(self.path) as conn:
            if not params:
                params = tuple()
            result = conn.execute(query, params)
            result.row_factory = sqlite3.Row
            data = result.fetchall()
            return [dict(r) for r in data]

    # def clear_dishes(self):
    #     with sqlite3.connect(self.path) as conn:
    #         conn.execute("DELETE FROM reviews")
    #         conn.commit()