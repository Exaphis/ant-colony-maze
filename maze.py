import random

class Maze:
  def __init__(self, rows, cols):
    # No start or end needed because maze generation
    # will visit every cell of the maze.

    self.rows = rows
    self.cols = cols
    self.maze = [[False] * (2 * self.cols + 1)
                 for _ in range(2 * self.rows + 1)]

    self.generate()

  def __str__(self):
    out = ''
    for i in range(len(self.maze)):
      for j in range(len(self.maze[i])):
        # use 2 characters to make square in output
        if not self.maze[i][j]:
          out += '█' * 2
        else:
          out += '\033[31m██\033[0m'
      out += '\n'

    return out

  def pos_to_maze(self, pos):
    return (2 * pos[0] + 1, 2 * pos[1] + 1)

  def in_bounds(self, pos):
    return 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols

  def get_midpoint(self, maze_pos_1, maze_pos_2):
    return ((maze_pos_1[0] + maze_pos_2[0]) // 2,
            (maze_pos_1[1] + maze_pos_2[1]) // 2)

  def exists_path(self, pos_1, pos_2):
    mid = self.get_midpoint(self.pos_to_maze(pos_1), self.pos_to_maze(pos_2))
    return self.maze[mid[0]][mid[1]]

  def get_neighbors(self, pos, with_path=True):
    candidates = [(pos[0], pos[1] + 1), (pos[0], pos[1] - 1),
                  (pos[0] + 1, pos[1]), (pos[0] - 1, pos[1])]

    out = []
    for c in candidates:
      if self.in_bounds(c):
        if with_path and not self.exists_path(pos, c):
          continue

        out.append(c)
    return out

  def generate(self):
    visited = [[False] * self.cols for _ in range(self.rows)]

    stack = [(None, (0, 0))]
    while stack:
      prev_maze_pos, curr = stack.pop()

      if visited[curr[0]][curr[1]]:
        continue
      visited[curr[0]][curr[1]] = True

      maze_pos = self.pos_to_maze(curr)
      self.maze[maze_pos[0]][maze_pos[1]] = True

      # Use midpoint to connect visited cells
      if prev_maze_pos is not None:
        mid_pos = self.get_midpoint(maze_pos, prev_maze_pos)

        # middle cell should never be already connected
        assert(not self.maze[mid_pos[0]][mid_pos[1]])
        self.maze[mid_pos[0]][mid_pos[1]] = True

      neighbors = self.get_neighbors(curr, False)
      random.shuffle(neighbors)
      stack.extend([(maze_pos, n) for n in neighbors])

