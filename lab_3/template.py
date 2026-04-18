import numpy as np
import matplotlib.pyplot as plt
import random

def min_max_norm(val, min_val, max_val, new_min, new_max):
    return (val - min_val) * (new_max - new_min) / (max_val - min_val) + new_min

class Chromosome:
    def __init__(self, length, array: list = None):  
        if array is None:
            array = np.random.randint(2, size=length)
        self.genes = array
        self.length = length

    def decode(self, lower_bound, upper_bound, aoi):
        segment = self.genes[lower_bound:upper_bound]
        int_val = 0
        for i, j in enumerate(segment):  
            int_val += j * 2**i
        k = upper_bound - lower_bound
        max_val = 2**k - 1
        decoded = min_max_norm(int_val, 0, max_val, aoi[0], aoi[1])
        return decoded

    def mutation(self, probability):  
        for i, bit in enumerate(self.genes):
            if random.random() < probability:  
                self.genes[i] = 1 - bit

    def crossover(self, other):  
        genes1 = self.genes
        genes2 = other.genes
        point = random.randint(1, self.length - 1)
        new_genes1 = np.concatenate((genes1[:point], genes2[point:]))
        new_genes2 = np.concatenate((genes2[:point], genes1[point:]))
        return Chromosome(self.length, new_genes1), Chromosome(self.length, new_genes2)

def objective_function(*args):
    """Himmelblau's function for Group B."""
    x1, x2 = args
    return (x1**2 + x2 - 11)**2 + (x1 + x2**2 - 7)**2

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
        
        self.population = [Chromosome(self.chromosome_length) for _ in range(self.population_size)]

    def eval_objective_func(self, chromosome):
        args = []
        for i in range(self.obj_func_num_args):
            low = i * self.bits_per_arg
            high = (i + 1) * self.bits_per_arg
            args.append(chromosome.decode(low, high, self.aoi))
        return self.objective_function(*args)

    def tournament_selection(self):
        selected_parents = []
        for _ in range(self.population_size):
            candidates = random.sample(self.population, self.tournament_size)
            winner = min(candidates, key=lambda c: self.eval_objective_func(c))
            selected_parents.append(winner)
        return selected_parents

    def reproduce(self, parents):
        new_pop = []
        for i in range(0, self.population_size, 2):
            p1, p2 = parents[i], parents[i+1]
            if random.random() < self.crossover_probability:
                c1, c2 = p1.crossover(p2)
            else:
                c1, c2 = Chromosome(self.chromosome_length, p1.genes.copy()), Chromosome(self.chromosome_length, p2.genes.copy())
            
            c1.mutation(self.mutation_probability)
            c2.mutation(self.mutation_probability)
            new_pop.extend([c1, c2])
        return new_pop

    def plot_func(self, trace):

        trace = np.array(trace)
        x = np.linspace(self.aoi[0], self.aoi[1], 100)
        y = np.linspace(self.aoi[0], self.aoi[1], 100)
        X, Y = np.meshgrid(x, y)
        Z = self.objective_function(X, Y)

        plt.figure(figsize=(10, 8))
        plt.contour(X, Y, Z, levels=50, cmap='viridis')
        
        colors = plt.cm.Reds(np.linspace(0.4, 1.0, len(trace)))
        plt.scatter(trace[:, 0], trace[:, 1], c=colors, edgecolor='black', s=50)
        
        plt.title("Himmelblau's Function Optimization Trace")
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.show()

    def run(self):

        trace = []
        for _ in range(self.num_steps):
            best_ind = min(self.population, key=lambda c: self.eval_objective_func(c))
            
            best_x1 = best_ind.decode(0, self.bits_per_arg, self.aoi)
            best_x2 = best_ind.decode(self.bits_per_arg, self.chromosome_length, self.aoi)
            best_val = self.eval_objective_func(best_ind)
            
            trace.append((best_x1, best_x2, best_val))
            
            parents = self.tournament_selection()
            self.population = self.reproduce(parents)
        return trace

if __name__ == "__main__":
    ga = GeneticAlgorithm(
        chromosome_length=40,
        obj_func_num_args=2,
        objective_function=objective_function,
        aoi=[-5, 5],
        population_size=100,
        tournament_size=3,
        mutation_probability=0.05,
        crossover_probability=0.8,
        num_steps=50
    )

    history = ga.run()
    ga.plot_func(history)
    
    best = history[-1]
    print(f"Final Minimum: x1={best[0]:.4f}, x2={best[1]:.4f}, Value={best[2]:.6f}")
