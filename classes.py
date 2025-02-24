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
        return f"W: {self.wins} L: {self.losses} W/R: {self.winrate_string()}"


class Leaderboard:
    def __init__(self, leaderboard_name: str):
        self.leaderboard_name = leaderboard_name
        self.scores: dict[str, Score] = {}  # FIX: Move dictionary inside __init__

    def add_win(self, username: str):
        self.scores.setdefault(username, Score(username)).won()  # Simplified

    def add_loss(self, username: str):
        self.scores.setdefault(username, Score(username)).lost()  # Simplified

    def remove_win(self, username: str):
        if self.scores.get(username) and self.scores[username].wins > 0:
            self.scores[username].wins -= 1

    def remove_loss(self, username: str):
        if self.scores.get(username) and self.scores[username].losses > 0:
            self.scores[username].losses -= 1

    def remove_player(self, username: str):
        self.scores.pop(username, None)  # `.pop()` with `None` avoids KeyError

    def print_scores(self):
        print(f"\nLeaderboard: {self.leaderboard_name}")
        for username, score in self.scores.items():
            print(f"{username}: {score.leaderboard_score_string()}")
        print()

    def print_by_wins(self) -> str:
        if not self.scores:
            return f"No players found in {self.leaderboard_name}."

        ret_str = f"**{self.leaderboard_name} - Ranked by Wins**\n\n"
        sorted_scores = sorted(self.scores.values(), key=lambda x: x.wins, reverse=True)

        for score in sorted_scores:
            ret_str += f"{score.name}: {score.leaderboard_score_string()}\n"
        return ret_str

    def print_by_winrate(self) -> str:
        if not self.scores:
            return f"No players found in {self.leaderboard_name}."

        ret_str = f"**{self.leaderboard_name} - Ranked by Win Rate**\n\n"
        sorted_scores = sorted(self.scores.values(), key=lambda x: x.winrate(), reverse=True)

        for score in sorted_scores:
            ret_str += f"{score.name}: {score.leaderboard_score_string()}\n"
        return ret_str


def add_fake_data(board: Leaderboard) -> None:
    players = ["Vinny", "Vex", "Noon", "Dee", "Hangry", "Dr.Headshot"]

    for _ in range(50):
        board.add_win(randint(0, len(players) - 1))

    for _ in range(50):
        board.add_loss(randint(0, len(players) - 1))


def main():
    board = Leaderboard("Bananas In-House")
    add_fake_data(board)

    board.print_scores()
    print(board.print_by_wins())
    print(board.print_by_winrate())

    board.remove_player("Dee")
    print(board.print_by_winrate())


if __name__ == '__main__':
    main()
