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
                                        gameName TEXT NOT NULL PRIMARY KEY,
                                        creatorID INTEGER NOT NULL
                                        status TEXT NOT NULL);"""
        sql_create_attendances_table = """CREATE TABLE IF NOT EXISTS attendances (
                                            playerID INTEGER NOT NULL PRIMARY KEY,
                                            FOREIGN KEY (gameName) REFERENCES games (gameName),
                                            condition TEXT NOT NULL,
                                            role TEXT NOT NULL);"""
        if self.db is not None:
            self.__create_table(sql_create_games_table)
            self.__create_table(sql_create_attendances_table)
        else:
            print("Error! cannot create the database connection.")

    def create_game(self, name, member):
        self.db.execute("INSERT INTO games(gameName, creatorID, status) VALUES (?, ?, 'open')",
                        [name, member.id])
        self.db.commit()

    def add_attendee(self, game_name, member):
        self.db.execute("""INSERT INTO attendences(playerID, gameName, condition, role)
                            VALUES (?, ?, 'alive', 'player')""")
        self.db.commit()    

    def assign_role(self, game_name, member, role):
        self.db.execute("UPDATE attendences SET role=? WHERE gameName=? AND playerID=?",
                            [role, game_name, member.id])
        self.db.commit()

    def start_game(self, game_name):
        self.db.execute("UPDATE games SET status='running' WHERE gameName=?", [game_name])
        self.db.commit()

    def kill_player(self, game_name, member):
        self.db.execute("UPDATE attendances SET condition='dead' WHERE gameName=? AND playerID=?",
                            [game_name, member.id])
        self.db.commit()

    def delete_game(self, game_name):     
        self.db.execute("DELETE FROM attendances WHERE gameName=?", [game_name])
        self.db.execute("DELETE FROM games WHERE gameName=?", [game_name])
        self.db.commit()

    def get_alive_IDs(self, game_name):
        c = self.db.cursor()
        c.execute("SELECT playerID FROM attendances WHERE gameName=? AND condition='alive'",
                    [game_name])
        results = c.fetchall()

        if len(results) < 1:
            return None

        return [playerID for result in results for playerID in result]

    def get_all_IDs(self, game_name):
        c = self.db.cursor()
        c.execute("SELECT playerID FROM attendances WHERE gameName=?", [game_name])
        results = c.fetchall()

        if len(results) < 1:
            return None

        return [playerID for result in results for playerID in result]

    def get_ID(self, game_name, role):
        c = self.db.cursor()
        c.execute("SELECT playerID FROM attendances WHERE gameName=? AND role=?", [game_name, role])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def get_playing_IDs(self):
        c = self.db.cursor()
        c.execute("""SELECT playerID 
                    FROM attendances AS a 
                        JOIN games AS g ON g.gameName = a.gameName
                    WHERE g.status = 'running'""")
        c.fetchall()

        if len(results) < 1:
            return None

        return [playerID for result in results for playerID in result]

    def get_alive_roles(self, game_name):
        c = self.db.cursor()
        c.execute("SELECT role FROM attendences WHERE gameName=? AND condition='alive'", [game_name])
        results = c.fetchall()

        if len(results) < 1:
            return None

        return [role for result in results for role in result]

    def get_role(self, game_name, member):
        c = self.db.cursor()
        c.execute("SELECT role FROM attendances WHERE gameName=? AND playerID=?",
                    [game_name, member.id])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def get_condition(self, game_name, member):
        c = self.db.cursor()
        c.execute("SELECT condition FROM attendances WHERE gameName=? AND playerID=?",
                    [game_name, member.id])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def get_games(self):
        c = self.db.cursor()
        c.execute("SELECT gameName FROM games")
        results = c.fetchall()

        if len(results) < 1:
            return None

        return [name for result in results for name in result]

    def get_open_games(self):
        c = self.db.cursor()
        c.execute("SELECT gameName FROM games WHERE status='open'")
        results = c.fetchall()

        if len(results) < 1:
            return None

        return [name for result in results for name in result]

    def get_status(self, game_name):
        c = self.db.cursor()
        c.execute("SELECT status FROM games WHERE gameName=?", [game_name])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def get_creator(self, game_name):
        c = self.db.cursor()
        c.execute("SELECT creatorID FROM games WHERE gameName=?", [game_name])
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
