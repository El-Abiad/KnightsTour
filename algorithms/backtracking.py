from imports import KNIGHT_MOVES
from imports import in_bounds, get_valid_neighbors


def order_children(
    children: list[tuple[int, int]],
    visited: set[tuple[int, int]],
    n: int ) -> list[tuple[int, int]]:
    scored = []
    for child in children:
        next_visited = visited | {child}
        onward_count = len(get_valid_neighbors(child, next_visited, n))
        scored.append((onward_count, child))
    scored.sort(key=lambda item: item[0])
    return [child for _, child in scored]


def knightstour_backtrack(n: int, start: tuple[int, int] = (0, 0)) -> list[tuple[int, int]] | None:
    if n <= 0 or not in_bounds(start[0], start[1], n):
        return None

    path = [start]
    visited = {start}

    def search(pos: tuple[int, int]) -> list[tuple[int, int]] | None:
        if len(path) == n * n:
            return path.copy()

        children = get_valid_neighbors(pos, visited, n)
        children = order_children(children, visited, n)

        for child in children:
            visited.add(child)
            path.append(child)

            result = search(child)
            if result is not None:
                return result

            path.pop()
            visited.remove(child)

        return None

    return search(start)


def backtracking_algorithm(n : int) -> list[tuple[int, int]] | None:
    return knightstour_backtrack(n, start=(0, 0))
