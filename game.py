import random
from gamelist import GameList

town_roles = ["inspector","doctor","drunk","bodyguard"]
mafia_roles = ["boss","disabler","stalker"]

class Game:
    instance = None

    def __init__(self):
        GameList.instance = GameList()
        
    def new_game(self, name, players, num_mafia, num_roles):
        author = players[0]
        gameID = GameList.instance.create_game(name, author)

        shuffled_players = random.shuffle(players)
        num_townies = len(players) - num_mafia

        for i in range(min(num_mafia, 3)):
            role = mafia_roles[i]
            player = shuffled_players[i]
            GameList.instance.create_attendance(player, gameID, role)
        for i in range(min(num_roles, 4)):
            role = town_roles[i]
            player = shuffled_players[num_mafia+i]
            GameList.instance.create_attendance(player, gameID, role)
        for player in shuffled_players[num_mafia+num_roles:]:
            GAmeList.instance.craete_attendance(player, gameID, "townie")

        return gameID

    def get_player_IDs(self, gameID, role):
        roles = GameList.instance.get_roles(gameID)
        players = []
        
        for role_pair in roles:
            temp_role, member = role_pair
            if temp_role == role:
                players.append(member)

        if len(players) == 1:
            return players[0]
        else:
            return players

    def kill_player(self, gameID, player):
        GameList.instance.kill_player(gameID, player)       

    def has_finished(self):
        if self.num_mafia <= 0:
            return "Town"
        elif self.num_townies <= 0:
            return "Mafia"
        else:
            return None