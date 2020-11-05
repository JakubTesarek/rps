import ai
import operator
from model import Result, Stats, Choice

class Controler:
    def __init__(self):
        self.ais = [
            ai.RandomAI(),
            ai.BeijingAlgorithmAI(),
            ai.MarkovChainAi(),
            ai.RandomBiasedAi(),
        ]
        self.stats = Stats()

    def play(self, player_choice):
        votes = {c: set() for c in Choice}
        for ai in self.ais:
            votes[ai.get_choice()].add(ai)

        top_choice = self.vote(votes)

        for ai_choice, voters in votes.items():
            for ai in voters:
                ai.add_result(Result(player_choice, top_choice, ai_choice))

        result = Result(player_choice, top_choice, top_choice)
        self.stats.add_result(result)
        return result

    def vote(self, votes):
        weights = {c: 0 for c in Choice}

        for choice, voters in votes.items():
            for ai in voters:
                weights[choice] += ai.win_rate

        return max(weights.items(), key=operator.itemgetter(1))[0]