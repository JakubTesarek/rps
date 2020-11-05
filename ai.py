from abc import ABC, abstractmethod
import random
from model import Choice, Stats


class AI(ABC):
    def __init__(self):
        self.stats = Stats()

    def add_result(self, result):
        self.stats.add_result(result)

    @property
    def win_rate(self):
        return self.stats.win_rate

    @property
    def loss_rate(self):
        return self.stats.loss_rate

    def random_choice(self):
        return random.choice(list(Choice))

    @abstractmethod
    def get_choice(self):
        pass

    def __str__(self):
        return type(self).__name__


class RandomAI(AI):
    def get_choice(self):
        return self.random_choice()


class BeijingAlgorithmAI(AI):
    def get_choice(self):
        try:
            result = self.stats.results[-1]
            ai_choice = result.ai_choice
            player_choice = result.player_choice
            if result.is_draw:
                return ai_choice.is_beaten
            for choice in Choice:
                if choice not in {ai_choice, player_choice}:
                    return choice
        except IndexError:
            return self.random_choice()


class MarkovChainAi(AI):
    def __init__(self):
        super().__init__()
        self.last_choice = None
        self.chain = {c1: {c2: 0 for c2 in Choice} for c1 in Choice}

    def add_result(self, result):
        super().add_result(result)
        if self.last_choice is not None:
            self.chain[self.last_choice][result.player_choice] += 1
        self.last_choice = result.player_choice

    def get_choice(self):
        if not self.last_choice:
            return self.random_choice()

        population = []
        weights = []
        for choice, count in self.chain[self.last_choice].items():
            population.append(choice)
            weights.append(count)

        expected = random.choices(
            population=population,
            weights=weights,
            k=1
        )[0]
        return expected.is_beaten


class RandomBiasedAi(AI):
    def __init__(self):
        super().__init__()
        self.bias = {c: 0 for c in Choice}

    def add_result(self, result):
        super().add_result(result)
        self.bias[result.player_choice] += 1

    def get_choice(self):
        population = []
        weights = []
        for choice, count in self.bias.items():
            population.append(choice)
            weights.append(count)

        expected = random.choices(
            population=population,
            weights=weights,
            k=1
        )[0]
        return expected.is_beaten