from path_finder import PathFinder

from collections import defaultdict
import random

class AntColonyOptimizationPathFinder(PathFinder):
  class Ant():
    def __init__(self, aco_instance, start, end):
      self.aco = aco_instance
      self.start = start
      self.end = end

    def generate_solution(self):
      curr = self.start
      path = [curr]
      trails_used = set()

      while curr != self.end:
        neighbors = self.aco.maze_obj.get_neighbors(curr)
        weights = [self.aco.pheromone_map[(curr, n)] for n in neighbors]

        # random.choices() with weights all 0 causes
        # it to output the last item
        if all(w == 0 for w in weights):
          weights = [1] * len(neighbors)

        src = curr
        curr = random.choices(neighbors, weights)[0]
        trails_used.add((src, curr))
        path.append(curr)

      for trail in trails_used:
        delta = self.aco.pheromone_constant / len(path)
        self.aco.pheromone_delta[trail] += delta

      return path


  def __init__(self, maze, num_ants=50, iterations=30,
               pheromone_evap_coeff=0.40, pheromone_constant=100.0):
    # ACO algorithms usually have an alpha and beta value
    # that determines whether pheromones or distance is
    # given more consideration.
    # In this case, distance is constant, so we have no
    # such values.

    self.iterations = iterations
    self.num_ants = num_ants
    self.pheromone_evap_coeff = float(pheromone_evap_coeff)
    self.pheromone_constant = float(pheromone_constant)

    # contains the pheromone level for (src, dst)
    self.pheromone_map = defaultdict(int)

    super().__init__(maze)

  def create_ant(self, start, end):
    return self.Ant(self, start, end)

  def find_path(self, start, end):
    ants = [self.create_ant(start, end) for _ in range(self.num_ants)]
    best_path = None
    best_path_length = float('inf')

    for i in range(self.iterations):
      # Generate ant paths
      print('starting iteration ' + str(i))
      self.pheromone_delta = defaultdict(int)
      for j, ant in enumerate(ants):
        print('  moving ant ' + str(j))
        path = ant.generate_solution()  # updates trail_freq
        if len(path) < best_path_length:
          best_path_length = len(path)
          best_path = path

      # Update pheromone values
      for trail in self.pheromone_map:
        self.pheromone_map[trail] *= (1 - self.pheromone_evap_coeff)
      for trail, delta in self.pheromone_delta.items():
        self.pheromone_map[trail] += delta

    print(self.pheromone_map)
    print('best path: ' + str(best_path_length))
    print(best_path)
    return best_path

