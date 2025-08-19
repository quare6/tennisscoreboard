class Player:
    def __init__(self, name, db_id):
        self.name = name
        self.points = 0
        self.games = 0
        self.sets = 0
        self.has_advantage = False
        self.db_id = db_id
