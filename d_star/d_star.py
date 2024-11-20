import argparse
import cv2
import numpy as np
import random
import heapq
import numpy as np

# Select random start and goal in free space
def selectPoints(map):
  """
  Selects random start and goal points in the free (white) spaces of the map.
  """
  # Find all white spaces
  free_spaces = np.unique(np.argwhere(map == 255)[:,0:2], axis=0)
  # Remove duplicate arrays
  free_spaces = np.unique(free_spaces, axis=0)
  # Swap columns to get (x, y) format
  free_spaces[:, [1, 0]] = free_spaces[:, [0, 1]]
  print("Free spaces shape:", str(free_spaces.shape))
  print("Free spaces # 1:", str(free_spaces[0]))
  print("Free spaces # 2:", str(free_spaces[1]))
  print("Free spaces # 3:", str(free_spaces[2]))
  print("Free spaces # 4:", str(free_spaces[3]))
  spaces = list(free_spaces)
  print("Free spaces list length:", len(spaces))
  print("Spaces # 1:", str(spaces[0]))
  start, goal = random.sample(list(free_spaces), 2)
  print("Start point:", start, "(green)")
  print("Start point background color:", map[start[1]][start[0]])
  cv2.circle(map, (start[0], start[1]), 10, (0, 255, 0), -1) # Start in green
  print("Goal point:", goal, "(blue)")
  print("Goal point background color:", map[goal[1]][goal[0]])
  cv2.circle(map, (goal[0], goal[1]), 10, (255, 0, 0), -1) # Start in blue

  return tuple(start), tuple(goal)

def dStar(map, start: cv2.typing.Point, goal: cv2.typing.Point) -> list:
  """
  Implement the D* algorithm to find the shortest path in the given map.

  @param map: The map image with obstacles
  @param start: The start position
  @param goal: The goal position
  @return: The path found by the D* algorithm
  """
  print(str(map.shape))
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
        and map[neighbor][2] == 255
      ):
        new_cost = cost_so_far[current] + 1

        if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
          cost_so_far[neighbor] = new_cost
          priority = new_cost + heuristic(goal, neighbor)
          heapq.heappush(open_list, (priority, neighbor))
          came_from[neighbor] = current

  # Reconstruct path
  path = []

  print("Goal:", goal)
  
  if goal in came_from:
    current = goal

    while current != start:
      path.append(current)
      current = came_from[current]
    
    path.append(start)
    path.reverse()
  
  return path

# Heuristic (Manhattan distance)
def heuristic(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])
