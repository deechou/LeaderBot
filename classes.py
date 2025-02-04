from random import randint


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
        if self.wins + self.losses == 0:
            return 0
        return self.wins / (self.wins + self.losses)
    def winrate_string(self) -> str:
        return f"{self.winrate()*100:.2f}%"
    def score_string(self) -> str:
        return f"{self.name} has {self.wins} wins and {self.losses} losses with a winrate of {self.winrate_string()}%"
    def leaderboard_score_string(self) -> str:
        return f"W: {self.wins} L: {self.losses} W/R: {self.winrate_string()}%"


class Leaderboard:
    scores: dict[str, Score] = {}

    def __init__(self, leaderboard_name: str):
        self.leaderboard_name = leaderboard_name

    def add_win(self, username: str):
        if username not in self.scores.keys():
            self.scores[username] = Score(username, 1, 0)
        else:
            self.scores[username].won()

    def add_loss(self, username: str):
        if username not in self.scores.keys():
            self.scores[username] = Score(username, 0, 1)
        else:
            self.scores[username].lost()

    def remove_win(self, username: str):
        if username not in self.scores.keys():
            return
        else:
            if self.scores[username].wins > 0:
                self.scores[username].wins -= 1


    def remove_loss(self, username: str):
        if username not in self.scores.keys():
            return
        else:
            if self.scores[username].losses > 0:
                self.scores[username].losses -= 1

    def remove_player(self, username: str):
        if username not in self.scores.keys():
            return
        else:
            self.scores.pop(username)

    def print_scores(self):
        print(f"These are the records for the leaderboard named {self.leaderboard_name}\n")
        for username in self.scores.keys():
            print(f"{username}: {self.scores[username].leaderboard_score_string()}")
        print("\n")

    def print_by_wins(self) -> str:
        ret_str = ""
        ret_str += f"This is the current standings for {self.leaderboard_name} ranked by wins\n\n"
        sorted_dict = dict(sorted(self.scores.items(), key=lambda item: item[1].wins, reverse=True))
        for username in sorted_dict.keys():
            ret_str +=(f"{username}: {sorted_dict[username].leaderboard_score_string()}\n")
        ret_str +=("\n")
        return ret_str

    def print_by_winrate(self):
        ret_str = ""
        ret_str += f"This is the current standings for {self.leaderboard_name} ranked by winrate\n\n"
        sorted_dict = dict(sorted(self.scores.items(), key=lambda item: item[1].winrate(), reverse=True))
        for username in sorted_dict.keys():
            ret_str += f"{username}: {sorted_dict[username].leaderboard_score_string()}\n"
        ret_str += "\n"
        return ret_str

def add_fake_data(board: Leaderboard) -> None:
    players = ["Vinny", "Vex", "Noon", "Dee", "Hangry", "Dr.Headshot"]
    counter = 0
    while counter < 50:
        board.add_win(players[randint(0, len(players) - 1)])
        counter+= 1
    counter = 0
    while counter < 50:
        board.add_loss(players[randint(0, len(players) - 1)])
        counter+= 1


def main():
    # test stuff here
    board = Leaderboard("bananas inhouse")
    add_fake_data(board)

    board.print_scores()
    print(board.print_by_wins())
    print(board.print_by_winrate())

if __name__ == '__main__':
    main()