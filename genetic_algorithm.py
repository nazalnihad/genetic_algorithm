from random import choices, randint, randrange, random

def generate_genome(length):
    return choices([0,1], k=length)

def generate_population(size, genome_length):
    return [generate_genome(genome_length) for _ in range(size)]

def single_point_crossover(a, b):
    if len(a) != len(b):
        raise ValueError("genome length are not same")

    length = len(a)
    if length < 2: #splits only if genome lenght > 2
        return a, b
    
    partition = randint(1, length-1) 
    # partition and crossover b/w genomes
    return a[0:partition] + b[partition:], b[0:partition] + a[partition:]

def mutation(genom, iter=1, probability=0.5):
    for _ in range(iter):
        index = randrange(len(genom))
        # mutate if probability > random generated probability i.e flips 1/0
        genom[index] = genom[index] if random() > probability else abs(genom[index] - 1)
    return genom

def population_fitness(population, fitness_func):
    return sum([fitness_func(genome) for genome in population])

def select_pairs(population, fitness_func):
    # select 2 best pairs
    return choices(
        population=population,
        weights=[fitness_func(gene) for gene in population],
        k=2
    )

def sort_population(population, fitness_func):
    return sorted(population, key=fitness_func, reverse=True)

def genome_to_string(genome):
    return "".join(map(str, genome))

def print_stats(population, generation_id, fitness_func):
    print("GENERATION %02d" % generation_id)
    print("=============")
    print("Population: [%s]" % ", ".join([genome_to_string(gene) for gene in population]))
    print("Avg. Fitness: %f" % (population_fitness(population, fitness_func) / len(population)))
    sorted_population = sort_population(population, fitness_func)
    print(
        "Best: %s (%f)" % (genome_to_string(sorted_population[0]), fitness_func(sorted_population[0])))
    print("Worst: %s (%f)" % (genome_to_string(sorted_population[-1]),
                              fitness_func(sorted_population[-1])))
    print("")

    return sorted_population[0]

def run_evolution(populate_func, fitness_func, fitness_limit, selection_func=select_pairs,
                  crossover_func=single_point_crossover, mutation_func=mutation,
                  generation_limit=100, printer=None):
    # random genomes made
    population = populate_func()

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if printer is not None:
            printer(population, i, fitness_func)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_gen = population[0:2]

        for j in range(int(len(population)/2)-1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_gen += [offspring_a, offspring_b]

        population = next_gen
    return population, i



# Example 
def example_fitness_function(genome):
    return sum(genome)

if __name__ == "__main__":
    population, generations = run_evolution(
        populate_func=lambda: generate_population(10, 8),
        fitness_func=example_fitness_function,
        fitness_limit=8,
        printer=print_stats
    )
    print("Evolution finished after %d generations." % generations)
