from algorithms.imports import KNIGHT_MOVES
from algorithms.imports import in_bounds, get_valid_neighbors


def knights_tour(n: int, start: tuple[int, int] = (0, 0)) -> list[tuple[int, int]] | None:
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