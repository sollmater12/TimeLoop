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
            password INT NOT NULL
        );"""
        self.cursor.execute(make_table)
        self.id = 0

    def check_user(self, name, password):
        request = """SELECT id, name, password FROM users WHERE name = ? AND password = ?"""
        result = self.cursor.execute(request, (name, password)).fetchall()
        if len(result) == 1:
            self.id = int(list(result)[0][0])
            self.connection.commit()
            return True
        return False

    def registration(self, name, password):
        if not self.check_user(name, password):
            request = """INSERT INTO users(name, password) VALUES(?, ?)"""
            result = self.cursor.execute(request, (name, password))
            if result:
                self.make_record_check(name)
                self.connection.commit()
                return True
            return False
        return False

    def make_record_check(self, name):
        req = """CREATE TABLE IF NOT EXISTS records (
    id     TEXT PRIMARY KEY
                UNIQUE
                NOT NULL,
    record INT  NOT NULL,
    moneys INT  NOT NULL
);
"""
        self.cursor.execute(req)
        request = """SELECT id FROM users WHERE name = ?"""
        result = self.cursor.execute(request, (name,)).fetchone()
        request = """INSERT INTO records(id, record, moneys) VALUES(?, ?, ?)"""
        self.cursor.execute(request, (result[0], 0, 0))
        self.id = result[0]

    def show_records(self):
        request = """SELECT record FROM records WHERE id = ?"""
        result = self.cursor.execute(request, (self.id,)).fetchall()
        return result[0][0]

    def show_money(self):
        request = """SELECT moneys FROM records WHERE id = ?"""
        result = self.cursor.execute(request, (self.id,)).fetchall()
        return result[0][0]

    def add_money(self, money):
        request = """SELECT moneys FROM records WHERE id = ?"""
        result = self.cursor.execute(request, (self.id,)).fetchone()
        check_money = money + int(result[0])
        request = """UPDATE records SET moneys = ? WHERE id = ?"""
        self.cursor.execute(request, (check_money, self.id))
        self.connection.commit()


    def check_record(self, record):
        request = """SELECT record FROM records WHERE id = ?"""
        result = self.cursor.execute(request, (self.id,)).fetchone()
        if record > int(result[0]):
            request = """UPDATE records SET record = ? WHERE id = ?"""
            self.cursor.execute(request, (record, self.id))
            self.connection.commit()
