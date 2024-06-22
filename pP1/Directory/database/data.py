import os
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

avatar_id = 'AgACAgIAAxkBAAIBB2ZrBpV45HmJKr4ngYtCJnCSGl8RAAKA3DEbD5pQS9IQbOYAARLbZwEAAwIAA3kAAzUE'

class DataBase:
    def __init__(self):
        db_path = 'Directory/database/accounts.db'
        db_dir = os.path.dirname(db_path)

        # Создаем каталог, если он не существует
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        # Создаем файл базы данных, если он не существует
        if not os.path.exists(db_path):
            open(db_path, 'w').close()

        self.conn = sqlite3.connect(db_path, timeout=5, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        name TEXT DEFAULT "TChatUser",
                        balance1 INTEGER DEFAULT 0,
                        balance2 INTEGER DEFAULT 0,
                        owner_id INTEGER DEFAULT 0,
                        cost INTEGER DEFAULT 50,
                        slaves TEXT DEFAULT "",
                        user_info TEXT,
                        avatar_id TEXT DEFAULT "{avatar_id}",
                        last_time_farm INTEGER DEFAULT 0,
                        premium1 INTEGER DEFAULT 0,
                        cookie INTEGER DEFAULT 0)''')

    def get_db(self, data):
        if data == "cursor":
            return self.cursor
        elif data == "conn":
            return self.conn
        else:
            print("Вы передали не conn/cursor")

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        if result.fetchone() is None:
            return False  # Его нет в базе данных
        else:
            return True  # Он есть в базе данных

    def reg_user(self, user_id):
        user_exists = self.user_exists(user_id)
        if not user_exists:
            self.cursor.execute(
                "INSERT INTO users (user_id, user_info, avatar_id) VALUES (?, ?, ?)",
                (user_id, 'не задано', avatar_id))
            self.conn.commit()

    def get_data(self, user_id: int, data: str):
        user_exists = self.user_exists(user_id)
        if not user_exists:
            self.reg_user(user_id=user_id)
        else:
            if data == "name":
                return self.cursor.execute("SELECT name FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
            elif data == "balance1":
                return self.cursor.execute("SELECT balance1 FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
            elif data == "balance2":
                return self.cursor.execute("SELECT balance2 FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
            elif data == "owner_id":
                return self.cursor.execute("SELECT owner_id FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
            elif data == "cost":
                return self.cursor.execute("SELECT cost FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
            elif data == "slaves":
                slaves = self.cursor.execute("SELECT slaves FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
                if slaves != "":
                    return list(slaves.split(" "))
                else:
                    return []
            elif data == "user_info":
                return self.cursor.execute("SELECT user_info FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
            elif data == "avatar_id":
                return self.cursor.execute("SELECT avatar_id FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
            elif data == "last_time_farm":
                return self.cursor.execute("SELECT last_time_farm FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
            elif data == "premium1":
                return self.cursor.execute("SELECT premium1 FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
            elif data == "cookie":
                return self.cursor.execute("SELECT cookie FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def edit_data_set(self, user_id: int, data: str, val):
        user_exists = self.user_exists(user_id)
        if not user_exists:
            self.reg_user(user_id=user_id)
        else:
            if data == "name":
                self.cursor.execute("UPDATE users SET name=? WHERE user_id=?", (val, user_id))
            elif data == "balance1":
                self.cursor.execute("UPDATE users SET balance1=? WHERE user_id=?", (val, user_id))
            elif data == "balance2":
                self.cursor.execute("UPDATE users SET balance2=? WHERE user_id=?", (val, user_id))
            elif data == "owner_id":
                self.cursor.execute("UPDATE users SET owner_id=? WHERE user_id=?", (val, user_id))
            elif data == "cost":
                self.cursor.execute("UPDATE users SET cost=? WHERE user_id=?", (val, user_id))
            elif data == "slaves":
                if val is None:
                    val = []
                val = " ".join(map(str, val))
                self.cursor.execute("UPDATE users SET slaves=? WHERE user_id=?", (val, user_id))
            elif data == "user_info":
                self.cursor.execute("UPDATE users SET user_info=? WHERE user_id=?", (val, user_id))
            elif data == "avatar_id":
                self.cursor.execute("UPDATE users SET avatar_id=? WHERE user_id=?", (val, user_id))
            elif data == "last_time_farm":
                self.cursor.execute("UPDATE users SET last_time_farm=? WHERE user_id=?", (val, user_id))
            elif data == "premium1":
                self.cursor.execute("UPDATE users SET premium1=? WHERE user_id=?", (val, user_id))
            elif data == "cookie":
                self.cursor.execute("UPDATE users SET cookie=? WHERE user_id=?", (val, user_id))
            self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()