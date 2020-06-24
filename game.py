import random

town_roles = ["inspector","doctor","drunk","bodyguard"]
mafia_roles = ["boss","disabler","stalker"]

class Game:
    def __init__(self, players, num_mafia, num_roles):
        self.players = random.shuffle(players)
        self.setup = {}

        for i in range(min(num_mafia, 3)):
            role = mafia_roles[i]
            self.setup[role] = self.players[i]
        for i in range(min(num_roles, 4)):
            role = town_roles[i]
            self.setup[role] = self.players[num_mafia+i]

        self.setup["townie"] = self.players[num_mafia+num_roles:]

    def has_finished(self):
        pass
