KNIGHT_MOVES = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
]

def in_bounds(r: int, c: int, n: int) -> bool:
    return 0 <= r < n and 0 <= c < n


def get_valid_neighbors(pos: tuple[int, int], visited: set[tuple[int, int]], n: int) -> list[tuple[int, int]]:
    r, c = pos
    neighbors = []
    for dr, dc in KNIGHT_MOVES:
        nr, nc = r + dr, c + dc
        nxt = (nr, nc)
        if in_bounds(nr, nc, n) and nxt not in visited:
            neighbors.append(nxt)
    return neighbors