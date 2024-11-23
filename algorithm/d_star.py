import cv2
import heapq
import sys
import time

sys.path.append('./ai_robotics_final_project')

from utils.points import drawInitialPoints, heuristic

def executeDStar(
  map: list,
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

  print("Executing D* algorithm...")

  d_star_execution_time = 0
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

      # Verify that neighbor coordinate is within bounds and not an obstacle
      if (
        0 <= neighbor[0] < rows
        and 0 <= neighbor[1] < cols
        and str(map[neighbor[1]][neighbor[0]]) != "[0 0 0]"
      ):
        new_cost = cost_so_far[current] + 1

        # If neighbor is not in cost_so_far or new_cost is less than
        # cost_so_far[neighbor], update came_from/cost_so_far and add neighbor
        # to open_list
        if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
          cost_so_far[neighbor] = new_cost
          priority = new_cost + heuristic(goal, neighbor)
          heapq.heappush(open_list, (priority, neighbor))
          came_from[neighbor] = current

  # Reconstruct path
  path = []
  
  if goal in came_from:
    # Record execution time
    end_time = time.time()
    d_star_execution_time = end_time - start_time
    current = goal

    while current != start:
      path.append((current[0], current[1]))
      current = came_from[current]
    
    path.append((start[0], start[1]))
    # Reverse path to get start to goal order
    path.reverse()

    print("Path found!")
    
    if verbose:
      print("Path length:", len(path))
  
  else:
    # Record execution time
    end_time = time.time()
    d_star_execution_time = end_time - start_time

    print("No path found!")
  
  drawInitialPoints(map, start, goal)

  print("D* execution time:", round(d_star_execution_time, 6), "seconds")
  print()

  return path

def executeDStarReplanning(
  map: list,
  path: list,
  start: cv2.typing.Point,
  goal: cv2.typing.Point,
  verbose: bool = False
) -> list:
  """
  D* replanning algorithm to find the shortest path in the given map, using RRT
  to get around obstacles.

  @param map: The map image with obstacles
  @param path: The path found by the D* algorithm
  @param start: The start position
  @param goal: The goal position
  @param verbose: Whether or not to print verbose output (default is False)
  @return: The path found by the D* replanning algorithm
  """

  #TODO: Implement D* replanning

  return path
