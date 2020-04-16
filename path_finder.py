from abc import ABC, abstractmethod

class PathFinder(ABC):
  def __init__(self, maze):
    self.maze_obj = maze
    self.path = self.find_path((0, 0),
                               (self.maze_obj.rows - 1, self.maze_obj.cols - 1))

  def __str__(self):
    path_set = set()
    for i in range(1, len(self.path)):
      prev = self.maze_obj.pos_to_maze(self.path[i - 1])
      curr = self.maze_obj.pos_to_maze(self.path[i])
      path_set.add(prev)
      path_set.add(self.maze_obj.get_midpoint(prev, curr))
      path_set.add(curr)

    out = ''
    for i in range(len(self.maze_obj.maze)):
      for j in range(len(self.maze_obj.maze[i])):
        # use 2 characters to make square in output
        if not self.maze_obj.maze[i][j]:
          out += '█' * 2
        elif (i, j) in path_set:
          out += '\033[32m██\033[0m'
        else:
          out += '\033[31m██\033[0m'
      out += '\n'

    return out

  @abstractmethod
  def find_path(self, start, end):
    pass

