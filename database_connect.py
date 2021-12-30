import sqlite3


class Connection():
    def __init__(self):
        self.connection = sqlite3.connect('data/databases/TimeLoop.sqlite')
        self.cursor = self.connection.cursor()
        make_table = """CREATE TABLE IF NOT EXISTS users (
            id       INT  PRIMARY KEY
                          UNIQUE
                          NOT NULL,
            name     TEXT UNIQUE
                          NOT NULL,
            password INT  UNIQUE
                          NOT NULL
        );"""
        self.cursor.execute(make_table)

    def check_user(self, name, password):
        request = """SELECT name, password FROM users WHERE name = ? AND password = ?"""
        result = self.cursor.execute(request, (name, password)).fetchall()
        if len(result) == 1:
            self.connection.commit()
            return True
        return False

    def registration(self, name, password):
        request = """INSERT INTO users(name, password) VALUES(?, ?)"""
        result = self.cursor.execute(request, (name, password))
        if result:
            self.connection.commit()
            return True
        return False
