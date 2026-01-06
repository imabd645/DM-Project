# Maaz Generator and Algorithm Visualizer

A terminal-based visualization tool that compares three pathfinding algorithms (DFS, BFS, and A*) solving randomly generated mazes in real-time.

## Features

- Real-time visualization of three pathfinding algorithms
- Performance comparison with metrics (explored cells, path length, execution time)
- Randomly generated mazes using recursive backtracker algorithm
- No external dependencies required

## Installation

Requires Python 3.6 or higher.

```bash
git clone https://github.com/imabd645/DM-Project.git
cd DM-Project
python maze_solver.py
```

## Algorithms

**DFS (Depth-First Search)** - Uses a stack to explore deep into paths before backtracking. May not find the shortest path.

**BFS (Breadth-First Search)** - Uses a queue to explore level by level. Guarantees the shortest path.

**A* (A-Star)** - Uses a heuristic (Manhattan distance) to intelligently guide the search. Most efficient for finding the shortest path.

## Configuration

Edit these constants in the script to customize:

```python
WIDTH = 35      # Maze width (must be odd)
HEIGHT = 17     # Maze height (must be odd)
SPEED = 0.1     # Animation speed in seconds
```

## Output

The program displays each algorithm solving the same maze with:
- Live visualization of the search process
- Final path highlighted
- Performance comparison table showing explored cells, path length, and execution time

