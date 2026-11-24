import random

from imports import get_valid_neighbors, is_neighbor



def fitness(path):
    return len(path)

def generate_path(pos: tuple[int, int], n: int):
    path = [pos]
    visited = {pos}

    while True:
        neighbors = get_valid_neighbors(pos, visited, n)

        if not neighbors: 
            break

        pos = random.choice(neighbors)
        path.append(pos)
        visited.add(pos)

    return path


def initialize_population(pop_size: int, n: int):
    population = []
    for _ in range(pop_size):
        population.append(generate_path((0, 0), n))

    return population

def selection(population: list):
    parents = random.sample(population, min(5, len(population)))
    parents.sort(key=fitness, reverse=True)
    return parents[:2]

def crossover(parent1: list, parent2: list, n: int):
    offspring = [(0, 0)]
    visited = {(0, 0)}
    current = (0, 0)

    ind1 = ind2 = 0

    while True:
        found = False
        choice = random.randint(0, 1)

        if (choice == 0 and ind1 < len(parent1) and 
            is_neighbor(current, parent1[ind1]) and
            parent1[ind1] not in visited):
            candidate = parent1[ind1]
            ind1 += 1

        elif ind2 < len(parent2):
            candidate = parent2[ind2]
            ind2 += 1

        else:
            candidate = None

        if (candidate is not None
                and is_neighbor(current, candidate)
                and candidate not in visited):
            current = candidate
            offspring.append(current)
            visited.add(current)
            found = True

        if not found:
            neighbors = get_valid_neighbors(current, visited, n)

            if not neighbors:
                break

            current = random.choice(neighbors)
            offspring.append(current)
            visited.add(current)

    return offspring


def mutation(path: list, mutation_rate: float, n: int):
    if random.random() < mutation_rate:
        cut = random.randint(1, len(path)-1)
        path = path[:cut]
        visited = set(path)
        pos = path[-1]
        while True:
                
                neighbors = get_valid_neighbors(pos, visited, n)
        
                if not neighbors: 
                    break
        
                pos = random.choice(neighbors)
                path.append(pos)
                visited.add(pos)

    return path



def remove_bad(population: list):
    population = sorted(population, key=fitness, reverse=True)
    population.pop()
    return population

def get_best(population: list):
    return max(population, key=fitness)

def genetic_algorithm(pop_size: int, n: int, generations: int, mutation_rate: float):
    population = initialize_population(pop_size, n)

    while(generations):
        best = get_best(population)

        if fitness(best) == n * n:
            return best
        
        parents = selection(population)
        parent1 = parents[0]
        parent2 = parents[1]

        offspring = crossover(parent1, parent2, n)
        offspring = mutation(offspring, mutation_rate, n)
        population.append(offspring)
        population = remove_bad(population)
        generations -= 1

    return get_best(population)


