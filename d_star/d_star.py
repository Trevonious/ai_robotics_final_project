import cv2
import heapq
import numpy as np
import random
import time

# Select random start and goal in free space
def selectPoints(map, verbose: bool = False) -> tuple:
  """
  Selects random start and goal points in the free (white) spaces of the map.

  @param map: The map image with obstacles
  @param verbose: Whether or not to print verbose output (default is False)
  @return: The start and goal points in the map
  """

  print("Randomly selecting start and goal points...")

  # Find all white spaces
  free_spaces = np.unique(np.argwhere(map == 255)[:,0:2], axis=0)
  # Remove duplicate arrays
  free_spaces = np.unique(free_spaces, axis=0)
  # Swap columns to get (x, y) format
  free_spaces[:, [1, 0]] = free_spaces[:, [0, 1]]
  start, goal = random.sample(list(free_spaces), 2)
  # Start point in green
  cv2.circle(map, (start[0], start[1]), 10, (0, 255, 0), -1)
  # Goal point in blue
  cv2.circle(map, (goal[0], goal[1]), 10, (255, 0, 0), -1)

  print("Start and goal points selected!")

  if verbose:
    print("Start point (green): (" + str(start[0]) + ", " + str(start[1]) + ")")
    print("Goal point (blue): (" + str(goal[0]) + ", " + str(goal[1]) + ")")

  return (start[0], start[1]), (goal[0], goal[1])

def dStar(
  map,
  start: cv2.typing.Point,
  goal: cv2.typing.Point,
  verbose: bool = False
) -> list:
  """
  Implement the D* algorithm to find the shortest path in the given map.

  @param map: The map image with obstacles
  @param start: The start position
  @param goal: The goal position
  @param verbose: Whether or not to print verbose output (default is False)
  @return: The path found by the D* algorithm
  """

  start_time = time.time()
  rows, cols, rgb = map.shape
  open_list = []
  heapq.heappush(open_list, (0, start))  # (cost, position)
  came_from = {}
  cost_so_far = { start: 0 }

  while open_list:
    current_cost, current = heapq.heappop(open_list)

    if current == goal:
      break

    # Explore neighbors
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
      neighbor = (current[0] + dx, current[1] + dy)

      if (
        0 <= neighbor[0] < rows
        and 0 <= neighbor[1] < cols
        and str(map[neighbor[1]][neighbor[0]]) != "[0 0 0]"
      ):
        new_cost = cost_so_far[current] + 1

        if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
          cost_so_far[neighbor] = new_cost
          priority = new_cost + heuristic(goal, neighbor)
          heapq.heappush(open_list, (priority, neighbor))
          came_from[neighbor] = current

  # Reconstruct path
  path = []
  
  if goal in came_from:
    current = goal

    while current != start:
      path.append((current[0], current[1]))
      current = came_from[current]
    
    path.append((start[0], start[1]))
    # Reverse path to get start to goal
    path.reverse()

  end_time = time.time()
  total_d_star_run_time = end_time - start_time

  if verbose:
    print("Path length:", len(path))
    print("Total D* run time:", total_d_star_run_time, "seconds")

  return path

def heuristic(a, b) -> int:
  """
  Finds the Manhattan distance between two points.

  @param a: The first point
  @param b: The second point
  @return: The Manhattan distance between the two points
  """

  return abs(a[0] - b[0]) + abs(a[1] - b[1])
