from enum import Enum


class Choice(Enum):
    rock = 1
    paper = 2
    scissors = 3

    @property
    def beats(self):
        return {
            Choice.rock: Choice.scissors,
            Choice.paper: Choice.rock,
            Choice.scissors: Choice.paper
        }[self]

    @property
    def is_beaten(self):
        return {
            Choice.scissors: Choice.rock,
            Choice.rock: Choice.paper,
            Choice.paper: Choice.scissors
        }[self]

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        if self is other:
            return False
        return other.beats is self

    def __le__(self, other):
        if self is other:
            return True
        return other.beats is self

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self is other

    def __gt__(self, other):
        if self is other:
            return False
        return self.beats is other

    def __ge__(self, other):
        if self is other:
            return True
        return self.beats is other


class Result:
    def __init__(self, player_choice, ai_choice, virtual_choice):
        self.player_choice = player_choice
        self.ai_choice = ai_choice
        self.virtual_choice = virtual_choice

    @property
    def ai_wins(self):
        return self.player_choice < self.ai_choice

    @property
    def virtual_ai_wins(self):
        return self.player_choice < self.virtual_choice

    @property
    def player_wins(self):
        return self.player_choice > self.ai_choice

    @property
    def virtual_player_wins(self):
        return self.player_choice > self.virtual_choice

    @property
    def is_draw(self):
        return self.player_choice == self.ai_choice

    @property
    def is_virtual_draw(self):
        return self.player_choice == self.virtual_choice


class Stats:
    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    @property
    def resolved_games(self):
        return len(self.results) - self.draws

    @property
    def wins(self):
        wins = 0
        for result in self.results:
            if result.virtual_ai_wins:
                wins += 1
        return wins

    @property
    def loses(self):
        loses = 0
        for result in self.results:
            if result.virtual_player_wins:
                loses += 1
        return loses

    @property
    def draws(self):
        draws = 0
        for result in self.results:
            if result.is_virtual_draw:
                draws += 1
        return draws

    @property
    def win_rate(self):
        wins = self.wins
        games = self.resolved_games
        if games > 0:
            return wins / games
        return 0

    @property
    def loss_rate(self):
        win_rate = self.win_rate
        if self.resolved_games > 0:
            return 1 - self.win_rate
        return 0