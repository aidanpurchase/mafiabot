import sqlite3
from sqlite3 import Error

class GameList:
    instance = None

    def __init__(self):
        print("Connecting to local database file game_list.sqlite...")
        
        self.db = None
        try:
            self.db = sqlite3.connect("game_list.sqlite")
        except Error as e:
            print(e)
        
        sql_create_games_table = """CREATE TABLE IF NOT EXISTS games (
                                        gameID INTEGER NOT NULL PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        creatorID INTEGER NOT NULL
                                        status TEXT NOT NULL);"""
        sql_create_attendances_table = """CREATE TABLE IF NOT EXISTS attendances (
                                            playerID INTEGER NOT NULL PRIMARY KEY,
                                            FOREIGN KEY (gameID) REFERENCES games (gameID),
                                            condition TEXT NOT NULL,
                                            role TEXT NOT NULL);"""
        if self.db is not None:
            self.__create_table(sql_create_games_table)
            self.__create_table(sql_create_attendances_table)
        else:
            print("Error! cannot create the database connection.")

    def create_game(self, name, member):
        self.db.execute("INSERT INTO games(name, creatorID, status) VALUES (?, ?, ?)",
                        [name, member.id, "open"])
        self.db.commit()

    def create_attendance(self, member, gameID, role):
        self.db.execute("""INSERT INTO attendances(playerID, gameID, condition, role) 
                            VALUES (?, ?, ?, ?)""",
                            [member.id, gameID, "alive", role])
        self.db.commit()

    def close_game(self, gameID):
        self.db.execute("UPDATE games SET status=? WHERE gameID=?", ["closed", gameID])
        self.db.commit()

    def kill_player(self, gameID, member):
        self.db.execute("UPDATE attendances SET condition=? WHERE gameID=? AND playerID=?",
                            ["dead", gameID, member.id])
        self.db.commit()

    def get_role(self, gameID, member):
        c = self.db.cursor()
        c.execute("SELECT role FROM attendances WHERE gameID=? AND playerID=?", [gameID, member.id])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def get_condition(self, gameID, member):
        c = self.db.cursor()
        c.execute("SELECT condition FROM attendances WHERE gameID=? AND playerID=?",
                    [gameID, member.id])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def get_status(self, gameID):
        c = self.db.cursor()
        c.execute("SELECT status FROM games WHERE gameID=?", [gameID])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def get_creator(self, gameID):
        c = self.db.cursor()
        c.execute("SELECT creatorID FROM games WHERE gameID=?", [gameID])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def __create_table(self, create_table_sql):
        try:
            c = self.db.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
