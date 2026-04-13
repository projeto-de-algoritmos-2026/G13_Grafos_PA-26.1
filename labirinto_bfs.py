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

        for dr, dc in directions: # testa as direções e e cria nova posição.
            nr, nc = r + dr, c + dc
            if 0 < nr < rows and 0 < nc < cols and maze[nr][nc] == 1:
                maze[r + dr//2][c + dc//2] = 0
                carve(nr, nc)

    carve(1, 1) #começa no ponto 1
    return maze


def bfs(maze, start, end): # funcao BFS
    rows, cols = len(maze), len(maze[0])

    if maze[start[0]][start[1]] != 0 or maze[end[0]][end[1]] != 0: # verifica se inicio e fim sao validos
        return None

    queue = deque([start]) #controla ordem da busca(fila da bfs)
    visited = {start}     # evita revisitar (conj visitados)
    previous = {start: None}  #reconstrui o caminho (Guarda de onde cada nó veio)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # possiveis movimentos

    while queue:   # remove o primeiro da fila.
        current = queue.popleft() 

        if current == end:  #verifica Se chegou no destino
            path = [] # Reconstrói o caminho voltando pelo previous

            while current is not None:
                path.append(current)
                current = previous[current]

            return path[::-1]  # Inverte o caminho (do início ao fim). 


        for dr, dc in directions:  #explora os vizinhos e testa 

            r = current[0] + dr
            c = current[1] + dc
            neighbor = (r, c)

            if (0 <= r < rows and 0 <= c < cols and
                maze[r][c] == 0 and neighbor not in visited):
                visited.add(neighbor) #marca
                previous[neighbor] = current #salva o pai
                queue.append(neighbor) # add na fila

    return None # retorna none se nao encontrou nenum caminho

def draw_maze(maze, path, start, end): #desenha o labirinto e Faz cópia da matriz
    display = [row[:] for row in maze]

    if path:
        for r, c in path:
            display[r][c] = 2 #marca o caminho com valor 2 

    display[start[0]][start[1]] = 3 #marca com inicio 3 
    display[end[0]][end[1]] = 4 # fim 4

    plt.imshow(display) # Mostra o labirinto como imagem
    plt.title("Busca em Árvore no Labirinto")
    plt.show()


if __name__ == "__main__":
    maze = generate_maze(21, 21) # Cria labirinto 21x21.

    start = (1, 1) # Define incio
    end = (19, 19) # Define fim

    start_time = time.perf_counter() # Mede tempo da busca
    path = tree_search(maze, start, end) # Calcula tempo total
    end_time = time.perf_counter() # Mostra o tempo

    elapsed_time = end_time - start_time

    print(f"Tempo de execução: {elapsed_time:.6f} segundos")

    if path:   # Verifica resultado
        print("Menor Caminho encontrado!")
    else:
        print("Não há caminho.")

    draw_maze(maze, path, start, end)  # Desenha o labirinto final
