from random import randint


class Score:
    def __init__(self, name, wins=0, losses=0):
        self.name: str = name
        self.wins: int = wins
        self.losses: int = losses

    def won(self):
        self.wins += 1

    def lost(self):
        self.losses += 1

    def winrate(self):
        return self.wins / (self.wins + self.losses) if (self.wins + self.losses) > 0 else 0

    def winrate_string(self) -> str:
        return f"{self.winrate() * 100:.2f}%"

    def score_string(self) -> str:
        return f"{self.name} has {self.wins} wins and {self.losses} losses with a winrate of {self.winrate_string()}"

    def leaderboard_score_string(self) -> str:
        return f"\t{self.wins} \t{self.losses} \t{self.winrate_string()}"


class Leaderboard:
    def __init__(self, leaderboard_name: str, leaderboard_message: str = None):
        self.leaderboard_name = leaderboard_name
        self.scores: dict[str, Score] = {}  # FIX: Move dictionary inside __init__
        self.message: str = leaderboard_message

        if leaderboard_message is not None:
            if 'Leaderboard:' in leaderboard_message:
                for line in leaderboard_message.splitlines():
                    if len(line) > 0 and '**' not in line:
                        split_line = line.split('\t')
                        self.scores[split_line[0]] = Score(split_line[0], int(split_line[1]), int(split_line[2]))
            else:
                print('Leaderboard message malformed')

    def add_win(self, username: str):
        self.scores.setdefault(username, Score(username)).won()  # Simplified

    def add_loss(self, username: str):
        self.scores.setdefault(username, Score(username)).lost()  # Simplified

    def change_wins(self, username: str, wins: int):
        self.add_win(username)
        self.scores[username].wins = wins

    def change_losses(self, username: str, losses: int):
        self.add_loss(username)
        self.scores[username].losses = losses

    def remove_win(self, username: str):
        if self.scores.get(username) and self.scores[username].wins > 0:
            self.scores[username].wins -= 1

    def remove_loss(self, username: str):
        if self.scores.get(username) and self.scores[username].losses > 0:
            self.scores[username].losses -= 1

    def remove_player(self, username: str):
        self.scores.pop(username, None)  # `.pop()` with `None` avoids KeyError

    def print_scores(self) -> str:
        if not self.scores:
            return f"No players found in {self.leaderboard_name}."

        ret_str = f"**Leaderboard: {self.leaderboard_name}**\n\n"
        for username, score in self.scores.items():
            ret_str += f"{username}: {score.leaderboard_score_string()}"
        return ret_str

    def print_by_wins(self) -> str:
        if not self.scores:
            return f"No players found in {self.leaderboard_name}."

        ret_str = f"**Leaderboard: {self.leaderboard_name} - Ranked by Wins**\n\n"
        sorted_scores = sorted(self.scores.values(), key=lambda x: x.wins, reverse=True)

        for score in sorted_scores:
            ret_str += f"{score.name}: {score.leaderboard_score_string()}\n"
        return ret_str

    def print_by_winrate(self) -> str:
        if not self.scores:
            return f"No players found in {self.leaderboard_name}."

        ret_str = f"**Leaderboard: {self.leaderboard_name} - Ranked by Win Rate**\n\n"
        sorted_scores = sorted(self.scores.values(), key=lambda x: x.winrate(), reverse=True)

        for score in sorted_scores:
            ret_str += f"{score.name}: {score.leaderboard_score_string()}\n"
        return ret_str

    def add_fake_data(self) -> None:
        players = ["Vinny", "Vex", "Noon", "Dee", "Hangry", "Dr.Headshot"]

        for player in players:
            if player not in self.scores:
                self.scores.update({player: Score(player)})

            self.change_wins(player, randint(0, 100))
            self.change_losses(player, randint(0, 100))



def main():
    leaderboard_message = """**Leaderboard: Bananas In-House - Ranked by Win Rate**

Hangry: 	66 	4 	94.29%
Vex: 	51 	42 	54.84%
Dr.Headshot: 	49 	46 	51.58%
Vinny: 	10 	32 	23.81%
Noon: 	4 	50 	7.41%
Dee: 	12 	55 	7.41%"""
    board = Leaderboard("Bananas In-House", leaderboard_message)


    print(board.print_scores())
    print(board.print_by_wins())
    print(board.print_by_winrate())

    board.remove_player("Dee")
    print(board.print_by_winrate())


if __name__ == '__main__':
    main()
