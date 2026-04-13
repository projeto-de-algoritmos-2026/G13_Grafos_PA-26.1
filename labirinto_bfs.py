import random
import time
from collections import deque
import matplotlib

try:
    matplotlib.use('TkAgg')
except ImportError:
    matplotlib.use('Agg')

import matplotlib.pyplot as plt

def generate_maze(rows, cols):
    rows = rows if rows % 2 == 1 else rows + 1
    cols = cols if cols % 2 == 1 else cols + 1

    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve(r, c):
        maze[r][c] = 0
        directions = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(directions)

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 < nr < rows and 0 < nc < cols and maze[nr][nc] == 1:
                maze[r + dr//2][c + dc//2] = 0
                carve(nr, nc)

    carve(1, 1)
    return maze


def tree_search(maze, start, end):
    rows, cols = len(maze), len(maze[0])

    if maze[start[0]][start[1]] != 0 or maze[end[0]][end[1]] != 0:
        return None

    queue = deque([start])
    visited = {start}
    previous = {start: None}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current = queue.popleft()

        if current == end:
            path = []

            while current is not None:
                path.append(current)
                current = previous[current]

            return path[::-1]

        for dr, dc in directions:
            r = current[0] + dr
            c = current[1] + dc
            neighbor = (r, c)

            if (0 <= r < rows and 0 <= c < cols and
                maze[r][c] == 0 and neighbor not in visited):
                visited.add(neighbor)
                previous[neighbor] = current
                queue.append(neighbor)

    return None

def draw_maze(maze, path, start, end):
    display = [row[:] for row in maze]

    if path:
        for r, c in path:
            display[r][c] = 2

    display[start[0]][start[1]] = 3
    display[end[0]][end[1]] = 4

    plt.imshow(display)
    plt.title("Busca em Árvore no Labirinto")
    plt.show()


if __name__ == "__main__":
    maze = generate_maze(21, 21)

    start = (1, 1)
    end = (19, 19)

    start_time = time.perf_counter()
    path = tree_search(maze, start, end)
    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    print(f"Tempo de execução: {elapsed_time:.6f} segundos")

    if path:
        print("Menor Caminho encontrado!")
    else:
        print("Não há caminho.")

    draw_maze(maze, path, start, end)
