from maze import Maze
from dijkstra import DijkstraPathFinder
from ant_colony import AntColonyOptimizationPathFinder


maze = Maze(15, 25)
d = DijkstraPathFinder(maze)
print(d)
input()
a = AntColonyOptimizationPathFinder(maze)
print(a)

