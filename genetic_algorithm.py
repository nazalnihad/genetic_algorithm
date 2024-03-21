from random import choices, randint, randrange, random
from typing import List, Callable, Tuple, Optional

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
PrinterFunc = Callable[[Population, int, FitnessFunc], None]

def generate_genome(length :int):
    return choices([0,1],k=length) #returns random 0,1 values with length k

def generate_population(size :int,genome_length :int):
    return [generate_genome(genome_length) for _ in range(size)]

def single_point_crossover(a:Genome , b:Genome):
    if len(a)!=len(b):
        raise ValueError("genome length are not same")

    length = len(a)
    if length < 2:
        return a,b # meaningless to crossover with lenth < 2
    
    partition = randint(1,length-1)
    # take random partition and split and join to make new genome
    return a[0:partition]+b[partition:] , b[0:partition]+a[partition:]

def mutation(genom : Genome , iter :int =1 ,probability:float=0.5):
    for _ in range(iter):
        index = randrange(len(genom))
        # flips the 0/1 value by comparing random value generated
        genom[index] = genom[index] if random()>probability else abs(genom[index]-1)
    return genom

def population_fitness(population:Population,fitness_func:FitnessFunc):
    return sum([fitness_func(genome) for genome in population])
    # return values of population

def select_pairs(population:Population,fitness_func:FitnessFunc):
    # returns pair of two best fit according to its weights
    return choices(
        population=population,
        weights=[fitness_func(gene) for gene in population],
        k=2
    )

def sort_population(population:Population,fitness_func:FitnessFunc):
    return sorted(population,key=fitness_func,reverse=True)

def genome_to_string(genome: Genome) :
    return "".join(map(str, genome))

def print_stats(population: Population, generation_id: int, fitness_func: FitnessFunc):
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

def run_evolution(populate_func:PopulateFunc,
                  fitness_func:FitnessFunc,
                  fitness_limit:int,
                  selection_func:SelectionFunc=select_pairs,
                  crossover_func:CrossoverFunc=single_point_crossover,
                  mutation_func:MutationFunc=mutation,
                  generation_limit:int=100,
                  printer: Optional[PrinterFunc] = None,
                  ):
    population = populate_func()

    for i in range(generation_limit):
        population = sorted(population,key=lambda genome:fitness_func(genome),reverse=True)

        if printer is not None:
            printer(population,i,fitness_func)
        
        if fitness_func(population[0]) >= fitness_limit:
            break

        next_gen = population[0:2]

        for j in range(int(len(population)/2)-1):
            parents = selection_func(population,fitness_func)
            offspring_a,offspring_b = crossover_func(parents[0],parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_gen += [offspring_a,offspring_b]
        
        population = next_gen
    return population,i


# Example usage:
def example_fitness_function(genome: Genome) -> int:
    # Example fitness function that counts the number of ones in the genome
    return sum(genome)

if __name__ == "__main__":
    population, generations = run_evolution(
        populate_func=lambda: generate_population(10, 8),
        fitness_func=example_fitness_function,
        fitness_limit=8,
        printer=print_stats
    )
    print("Evolution finished after %d generations." % generations)
