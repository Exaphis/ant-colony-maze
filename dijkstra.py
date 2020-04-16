from path_finder import PathFinder

import heapq

class DijkstraPathFinder(PathFinder):
  def find_path(self, start, end):
    assert(self.maze_obj.in_bounds(start))
    assert(self.maze_obj.in_bounds(end))

    best_dist = [[float('inf')] * self.maze_obj.cols
                 for _ in range(self.maze_obj.rows)]
    prev = {}
    queue = []
    heapq.heappush(queue, (0, start))

    while queue:
      dist, curr = heapq.heappop(queue)
      if curr == end:
        break

      new_dist = dist + 1

      for neighbor in self.maze_obj.get_neighbors(curr):
        if new_dist < best_dist[neighbor[0]][neighbor[1]]:
          prev[neighbor] = curr
          best_dist[neighbor[0]][neighbor[1]] = new_dist

          heapq.heappush(queue, (new_dist, neighbor))

    assert(curr == end)

    path = []
    curr = end
    while curr != start:
      path.append(curr)
      curr = prev[curr]
    path.append(start)

    print('length: ' + str(len(path)))
    return list(reversed(path))

