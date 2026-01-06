import random
import time
import os
import heapq
from collections import deque

# --- UI CONSTANTS ---
# ANSI Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
DIM = '\033[2m'
RESET = '\033[0m'
BOLD = '\033[1m'
CLEAR = '\033[H'

# Symbols (Unicode Box Drawing)
WALL = f"{DIM}█{RESET}"
PATH = " "
START = f"{GREEN}◈{RESET}"
END = f"{RED}🏁{RESET}"
SCAN = f"{CYAN}◌{RESET}"
VSTD = f"{BLUE}·{RESET}"
STEP = f"{YELLOW}●{RESET}"

# Config
WIDTH = 35  # Must be odd
HEIGHT = 17  # Must be odd
SPEED = 0.1

# maze generator

def generate_maze(w, h):
    """Recursive Backtracker for a perfect maze."""
    grid = [[WALL] * w for _ in range(h)]
    
    def walk(r, c):
        grid[r][c] = PATH
        dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 1 <= nr < h-1 and 1 <= nc < w-1 and grid[nr][nc] == WALL:
                grid[r + dr//2][c + dc//2] = PATH
                walk(nr, nc)
    
    walk(1, 1)
    grid[1][1] = START
    grid[h-2][w-2] = END
    return [row[:] for row in grid]

# searching algorithms

def get_moves(maze, r, c):
    """Get valid neighboring moves."""
    h = len(maze)
    w = len(maze[0])
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < h and 0 <= nc < w:
            if maze[nr][nc] in (PATH, END):
                yield (nr, nc)

def draw_maze(maze, name, stats=""):
    """Draw the maze with borders and stats."""
    w = len(maze[0])
    buffer = [f"\n  {BOLD}{YELLOW}» {name}{RESET}"]
    # Draw top border
    buffer.append("  " + DIM + "┏" + "━" * (w * 2) + "┓" + RESET)
    for row in maze:
        line = "  " + DIM + "┃" + RESET
        for cell in row:
            line += cell + (" " if cell != WALL else WALL)
        line += DIM + "┃" + RESET
        buffer.append(line)
    buffer.append("  " + DIM + "┗" + "━" * (w * 2) + "┛" + RESET)
    buffer.append(f"  {DIM}{stats}{RESET}\033[J")
    
    print(CLEAR + "\n".join(buffer))
    time.sleep(SPEED)

def mark_cell(maze, pos, sym, start, end):
    """Mark a cell with a symbol if it's not start or end."""
    if pos != start and pos != end:
        maze[pos[0]][pos[1]] = sym

def get_path(parent, end):
    """Reconstruct path from parent dictionary."""
    path = []
    curr = end
    while curr in parent:
        path.append(curr)
        curr = parent[curr]
    return path[::-1]

def bfs_solve(base_maze, name):
    """BFS Solver."""
    maze = [row[:] for row in base_maze]
    h = len(maze)
    w = len(maze[0])
    start = (1, 1)
    end = (h-2, w-2)
    parent = {}
    explored = 0
    
    queue = deque([start])
    visited = {start}
    
    while queue:
        curr = queue.popleft()
        if curr == end:
            return maze, explored, get_path(parent, end)
        
        explored += 1
        mark_cell(maze, curr, SCAN, start, end)
        draw_maze(maze, name, f"Queue Size: {len(queue)} | Explored: {explored}")
        mark_cell(maze, curr, VSTD, start, end)
        
        for move in get_moves(maze, *curr):
            if move not in visited:
                visited.add(move)
                parent[move] = curr
                queue.append(move)
    
    return maze, explored, []

def dfs_solve(base_maze, name):
    """DFS Solver."""
    maze = [row[:] for row in base_maze]
    h = len(maze)
    w = len(maze[0])
    start = (1, 1)
    end = (h-2, w-2)
    parent = {}
    explored = 0
    
    stack = [start]
    visited = {start}
    
    while stack:
        curr = stack.pop()
        if curr == end:
            return maze, explored, get_path(parent, end)
        
        explored += 1
        mark_cell(maze, curr, SCAN, start, end)
        draw_maze(maze, name, f"Stack Depth: {len(stack)} | Explored: {explored}")
        mark_cell(maze, curr, VSTD, start, end)
        
        for move in get_moves(maze, *curr):
            if move not in visited:
                visited.add(move)
                parent[move] = curr
                stack.append(move)
    
    return maze, explored, []

def astar_solve(base_maze, name):
    """A* Solver."""
    maze = [row[:] for row in base_maze]
    h = len(maze)
    w = len(maze[0])
    start = (1, 1)
    end = (h-2, w-2)
    parent = {}
    explored = 0
    
    h_func = lambda p: abs(p[0]-end[0]) + abs(p[1]-end[1])
    open_set = [(h_func(start), 0, start)]
    g_score = {start: 0}
    
    while open_set:
        f, g, curr = heapq.heappop(open_set)
        if curr == end:
            return maze, explored, get_path(parent, end)
        
        explored += 1
        mark_cell(maze, curr, SCAN, start, end)
        draw_maze(maze, name, f"Priority Queue (f={f}) | Explored: {explored}")
        mark_cell(maze, curr, VSTD, start, end)

        for move in get_moves(maze, *curr):
            tent_g = g_score[curr] + 1
            if move not in g_score or tent_g < g_score[move]:
                g_score[move] = tent_g
                parent[move] = curr
                heapq.heappush(open_set, (tent_g + h_func(move), tent_g, move))
    
    return maze, explored, []

# comparison function

def run_comparison():
    os.system('cls' if os.name == 'nt' else 'clear')
    base_maze = generate_maze(WIDTH, HEIGHT)
    
    results = []
    solvers = [
        ("DFS (Deep Search)", dfs_solve),
        ("BFS (Shortest Path)", bfs_solve),
        ("A* (Optimized)", astar_solve)
    ]
    
    start = (1, 1)
    end = (HEIGHT-2, WIDTH-2)

    for label, solver_func in solvers:
        start_t = time.time()
        maze, explored, path = solver_func(base_maze, label)
        
        dur = time.time() - start_t
        
        if path:
            for p in path[:-1]:
                mark_cell(maze, p, STEP, start, end)
                draw_maze(maze, label, "Drawing Final Path...")
            results.append((label, explored, len(path), dur))
        time.sleep(1)

    # Final Summary Table
    print(f"\n  {BOLD}FINAL PERFORMANCE COMPARISON{RESET}")
    print("  " + "━" * 60)
    print(f"  {'Algorithm':<20} | {'Explored':<10} | {'Steps':<8} | {'Time'}")
    for name, exp, steps, dur in results:
        print(f"  {name:<20} | {exp:<10} | {steps:<8} | {dur:.2f}s")
    print("\n")

if __name__ == "__main__":
    try:
        run_comparison()
    except KeyboardInterrupt:
        print("\n  Stopped by user.")