import numpy as np
import matplotlib.pyplot as plt
import random


def min_max_norm(val, min_val, max_val, new_min, new_max):
    return (val - min_val) * (new_max - new_min) / (max_val - min_val) + new_min


class Chromosome:

    def __init__(self, length, array: list = None):  # if array is None, initialize with a random binary vector
        if array is None:
            array = np.random.randint(2, size=length)

        self.genes = array
        self.length = length

    def decode(self, lower_bound, upper_bound, aoi):
        # Decode the chromosome segment from bit lower_bound to bit upper_bound into a real number within range aoi. You may use the provided min_max_norm helper.
        segment = self.genes[lower_bound:upper_bound]
        int_val = 0
        for i, j in enumerate(segment):  # LITTLE OR BIG ENDIAN ?
            int_val += j * 2**i

        k = upper_bound - lower_bound
        max_val = 2**k - 1

        decoded = min_max_norm(int_val, 0, max_val, aoi[0], aoi[1])
        return decoded

    def mutation(self, probability):  # flip each bit with the given probability
        for i, bit in enumerate(self.genes):
            rando = random.randint(0, 10)
            if rando < probability * 10:  # hit
                self.genes[i] = 1 - bit
        pass

    def crossover(self, other):  # Perform one-point crossover with another chromosome. Return two offspring.
        genes1 = self.genes
        genes2 = other.genes
        point = random.randint(1, self.length - 1)
        new_genes1 = np.concatenate((genes1[:point], genes2[point:]))
        new_genes2 = np.concatenate((genes2[:point], genes1[point:]))
        return Chromosome(self.length, new_genes1), Chromosome(self.length, new_genes2)


def objective_function(*args):
    # f ( x 1 , x 2 ) = 20 + x 1 2 − 10 cos ⁡ ( 2 π x 1 ) + x 2 2 − 10 cos ⁡ ( 2 π x 2 )
    x1, x2 = args
    return 20 + x1**2 - 10 * np.cos(2 * np.pi * x1) + x2**2 - 10 * np.cos(2 * np.pi * x2)


class GeneticAlgorithm:
    def __init__(
        self,
        chromosome_length,
        obj_func_num_args,
        objective_function,
        aoi,
        population_size=100,
        tournament_size=2,
        mutation_probability=0.05,
        crossover_probability=0.8,
        num_steps=50,
    ):
        assert chromosome_length % obj_func_num_args == 0, "Number of bits for each argument should be equal"
        self.chromosome_length = chromosome_length
        self.obj_func_num_args = obj_func_num_args
        self.bits_per_arg = int(chromosome_length / obj_func_num_args)
        self.objective_function = objective_function
        self.aoi = aoi
        self.tournament_size = tournament_size
        self.mutation_probability = mutation_probability
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.num_steps = num_steps

    def eval_objective_func(self, chromosome):
        pass

    def tournament_selection(self):
        pass

    def reproduce(self, parents):
        pass

    def plot_func(self, trace):
        pass

    def run(self):
        pass


# TODO: fill in the parameters for your group and uncomment to run
# ga = GeneticAlgorithm(
#     chromosome_length=...,
#     obj_func_num_args=2,
#     objective_function=objective_function,
#     aoi=[...],
#     population_size=...,
#     tournament_size=2,
#     mutation_probability=0.05,
#     crossover_probability=0.8,
#     num_steps=...
# )
# ga.run()
