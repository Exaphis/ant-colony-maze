from path_finder import PathFinder

from collections import defaultdict
import random

class AntColonyOptimizationPathFinder(PathFinder):
  class Ant():
    def __init__(self, aco_instance, start, end):
      # Reduce node revisitation by making ant prefer to go
      # in one direction
      self.turn_right = {(0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0),
                         (-1, 0): (0, 1)}
      self.turn_left = {(0, 1): (-1, 0), (-1, 0): (0, -1), (0, -1): (1, 0),
                        (1, 0): (0, 1)}
      self.direction = (0, 1)

      self.aco = aco_instance
      self.start = start
      self.end = end

    def generate_solution(self):
      curr = self.start
      path = [curr]
      trails_used = set()

      while curr != self.end:
        left = self.turn_left[self.direction]
        right = self.turn_right[self.direction]

        neighbors = self.aco.maze_obj.get_neighbors(curr)
        weights = []
        for n in neighbors:
          delta = (n[0] - curr[0], n[1] - curr[1])
          if delta == self.direction:
            loss_mult = 1
          elif delta == left or delta == right:
            loss_mult = 1 - self.aco.direction_loss_coeff
          else:
            loss_mult = (1 - self.aco.direction_loss_coeff) ** 2

          weights.append(self.aco.pheromone_map[(curr, n)] * loss_mult)

        # random.choices() with weights all 0 causes
        # it to output the last item
        if all(w == 0 for w in weights):
          weights = [1] * len(neighbors)

        src = curr
        curr = random.choices(neighbors, weights)[0]
        trails_used.add((src, curr))
        path.append(curr)
        self.direction = (curr[0] - src[0], curr[1] - src[1])

      for trail in trails_used:
        delta = self.aco.pheromone_constant / len(path)
        self.aco.pheromone_delta[trail] += delta

      return path


  def __init__(self, maze, num_ants=1, iterations=30,
               pheromone_evap_coeff=0.40, pheromone_constant=1000.0,
               direction_loss_coeff=0.6):
    # ACO algorithms usually have an alpha and beta value
    # that determines whether pheromones or distance is
    # given more consideration.
    # In this case, distance is constant, so we have no
    # such values.

    self.iterations = iterations
    self.num_ants = num_ants
    self.pheromone_evap_coeff = float(pheromone_evap_coeff)
    self.pheromone_constant = float(pheromone_constant)
    self.direction_loss_coeff = float(direction_loss_coeff)

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
      #print('starting iteration ' + str(i))
      self.pheromone_delta = defaultdict(int)
      for j, ant in enumerate(ants):
        #print('  moving ant ' + str(j))
        path = ant.generate_solution()  # updates trail_freq
        if len(path) < best_path_length:
          best_path_length = len(path)
          best_path = path

      # Update pheromone values
      for trail in self.pheromone_map:
        self.pheromone_map[trail] *= (1 - self.pheromone_evap_coeff)
      for trail, delta in self.pheromone_delta.items():
        self.pheromone_map[trail] += delta

    #print(self.pheromone_map)
    print('best path: ' + str(best_path_length))
    #print(best_path)
    return best_path

