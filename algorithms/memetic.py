import random
import time

from imports import get_valid_neighbors, in_bounds

Position = tuple[int, int]
Path = list[Position]


def _fitness(path: Path) -> int:
    return len(path)

def _choose_next(
    current: Position,
    visited: set[Position],
    n: int,
    rng: random.Random,
    preferred: Position | None = None,
    randomness: float = 0.15,
) -> Position | None:
    neighbors = get_valid_neighbors(current, visited, n)
    if not neighbors:
        return None
    if preferred in neighbors:
        return preferred
    if randomness > 0 and rng.random() < randomness:
        return rng.choice(neighbors)

    onward = {
        square: len(get_valid_neighbors(square, visited, n)) for square in neighbors
    }
    best = min(onward.values())
    return rng.choice([square for square in neighbors if onward[square] == best])


def _grow(
    path: Path,
    n: int,
    rng: random.Random,
    preferred_edges: dict[Position, Position] | None = None,
    randomness: float = 0.15,
) -> Path:
    result = list(path)

    visited = set(result)
    current = result[-1]
    while len(result) < n * n:
        preferred = preferred_edges.get(current) if preferred_edges else None
        nxt = _choose_next(current, visited, n, rng, preferred, randomness)
        if nxt is None:
            break
        result.append(nxt)
        visited.add(nxt)
        current = nxt
    return result


def _regrow(
    path: Path,
    n: int,
    rng: random.Random,
    preferred_edges: dict[Position, Position] | None = None,
) -> Path:
    cut = rng.randint(1, max(1, len(path) - 1))
    return _grow(path[:cut], n, rng, preferred_edges)


def _improve(path: Path, n: int, rng: random.Random, iterations: int) -> Path:
    best = list(path)
    for _ in range(iterations):
        if len(best) >= n * n:
            break
        candidate = _regrow(best, n, rng)
        if len(candidate) > len(best):
            best = candidate
    return best


def _tournament(population: list[Path], rng: random.Random, size: int = 3) -> Path:
    return max(rng.sample(population, min(size, len(population))), key=_fitness)


def _crossover(parent1: Path, parent2: Path, n: int, rng: random.Random) -> Path:
    return _regrow(parent1, n, rng, dict(zip(parent2, parent2[1:])))


def _expired(deadline: float | None) -> bool:
    return deadline is not None and time.perf_counter() >= deadline


def memetic_algorithm(
    n: int,
    pop_size: int = 30,
    generations: int = 100,
    mutation_rate: float = 0.2,
    local_search_iters: int = 10,
    start: Position = (0, 0),
    seed: int | None = None,
    time_limit: float | None = None,
) -> Path:
    if n <= 0 or not in_bounds(start[0], start[1], n):
        return []
    if pop_size < 2:
        raise ValueError("pop_size must be at least 2")

    rng = random.Random(seed)
    target = n * n

    population = [_grow([start], n, rng, randomness=1.0) for _ in range(pop_size)]
    population.sort(key=_fitness, reverse=True)
    best = list(population[0])

    elite_count = min(2, pop_size - 1)
    deadline = None if time_limit is None else time.perf_counter() + time_limit

    for _ in range(generations):
        if len(best) >= target or _expired(deadline):
            break

        next_population = [list(path) for path in population[:elite_count]]
        while len(next_population) < pop_size and not _expired(deadline):
            child = _crossover(
                _tournament(population, rng), _tournament(population, rng), n, rng
            )
            if rng.random() < mutation_rate:
                child = _regrow(child, n, rng)
            child = _improve(child, n, rng, local_search_iters)
            if len(child) >= target:
                return child
            next_population.append(child)

        population = sorted(next_population, key=_fitness, reverse=True)
        if len(population[0]) > len(best):
            best = list(population[0])

    return best
