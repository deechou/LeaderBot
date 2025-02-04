from random import choice, randint

class Score:
    def __init__(self, name, wins, losses):
        self.name: str = name
        self.wins: int = wins
        self.losses: int = losses
    def won(self):
        self.wins += 1
    def lost(self):
        self.losses += 1
    def winrate(self):
        return self.wins / (self.wins + self.losses)
    def score_string(self):
        return f"{self.name} has {self.wins} wins and {self.losses} losses with a winrate of {self.winrate()}"



def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Nothing?'
    if 'hello' in lowered:
        return 'Hello there fellow banana!'
    if 'how are you' in lowered:
        return 'Good, thanks!'
    if 'bye' in lowered:
        return 'See ya!'
    if 'won' in lowered:
        return 'good job ' + lowered[0]
    if 'lost' in lowered:
        return 'aw shucks ' + lowered[0]
    if 'newplayer' in lowered:
        newplayername = lowered.split(' ')[1]
        p1 = Score(newplayername, 3, 2)
        return p1.score_string()