import copy

from player import Player
import numpy as np


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)
        players.sort(key=lambda x: x.fitness, reverse=True)
        # # TODO (Additional: Implement roulette wheel here)
        # players = self.roulette_wheel(players, num_players)
        # # TODO (Additional: Implement SUS here)
        # players = self.SUS(players, num_players)
        # # Q-tournament
        # players = self.Q_tournament(players, num_players)
        # # TODO (Additional: Learning curve)

        return players[: num_players]

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            # TODO ( Parent selection and child generation )
            parents = self.Q_tournament(prev_players, num_players)
            children = []
            for i in range(0, len(parents), 2):
                p = parents[i]
                q = parents[i + 1]
                child1, child2 = self.crossover(p, q)
                child1_mut = self.mutate(child1, 0.5)
                child2_mut = self.mutate(child2, 0.5)
                children.append(child1_mut)
                children.append(child2_mut)
            return children

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player

    def roulette_wheel(self, players, num_players):
        fitness_sum = sum([p.fitness for p in players])
        probs = [p.fitness / fitness_sum for p in players]
        for i in range(1, len(probs)):
            probs[i] = probs[i] + probs[i - 1]
        next_pop = []
        for i in range(num_players):
            r = np.random.uniform(0, 1)
            for j, p in enumerate(probs):
                if r <= p:
                    next_pop.append(players[j])
                    break
        return next_pop

    def SUS(self, players, num_players):
        fitness_sum = sum([p.fitness for p in players])
        probs = [p.fitness / fitness_sum for p in players]
        for i in range(1, len(probs)):
            probs[i] = probs[i] + probs[i - 1]
        next_pop = []
        N2 = 1.0 / num_players
        r = np.random.uniform(0, N2)
        for i in range(num_players):
            for j, p in enumerate(probs):
                if r <= p:
                    next_pop.append(players[j])
                    break
            r += N2
        return next_pop

    def Q_tournament(self, players, num_players):
        q = 2
        next_pop = []
        for i in range(num_players):
            q_random_players = np.random.choice(players, q)
            next_pop.append(max(q_random_players, key=lambda player: player.fitness))
        return next_pop

    def crossover(self, p, q):
        child1 = self.clone_player(p)
        child2 = self.clone_player(q)
        child1.nn.w1, child2.nn.w1 = self.cross(p.nn.w1, q.nn.w1)
        child1.nn.b1, child2.nn.b1 = self.cross(p.nn.b1, q.nn.b1)
        child1.nn.w2, child2.nn.w2 = self.cross(p.nn.w2, q.nn.w2)
        child1.nn.b2, child2.nn.b2 = self.cross(p.nn.b2, q.nn.b2)
        return child1, child2

    def mutate(self, child, thresh):
        prob = 0.25
        r = np.random.uniform(0, 1)
        if r >= prob:
            return child
        child.nn.w1 += np.random.normal(0, thresh, child.nn.w1.shape)
        child.nn.w2 += np.random.normal(0, thresh, child.nn.w2.shape)
        child.nn.b1 += np.random.normal(0, thresh, child.nn.b1.shape)
        child.nn.b2 += np.random.normal(0, thresh, child.nn.b2.shape)
        return child

    def cross(self, a, b):
        prob = 0.8
        r = np.random.uniform(0, 1)
        mid = int(a.shape[0] / 2)
        if r >= prob:
            return a, b
        ch1 = np.concatenate((a[:mid], b[mid:]), axis=0)
        ch2 = np.concatenate((b[:mid], a[mid:]), axis=0)
        return ch1, ch2
