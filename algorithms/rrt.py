import cv2
import numpy as np
import random
import time

# Check if the line between two points intersects obstacles
def isCollisionFree(
  map: list,
  point1: tuple,
  point2: tuple
) -> bool:
  """
  Checks if the line between two points is collision-free.

  @param map: The map image with obstacles
  @param point1: The first point
  @param point2: The second point
  @return: True if the line is collision-free, False otherwise
  """
  
  line = np.linspace(point1, point2, num=100, dtype=int)

  for x, y in line:

    if str(map[y][x]) == "[0 0 0]":  # Black pixel indicates obstacle
      return False
  
  return True

def executeRRT(
  map: list,
  start: cv2.typing.Point,
  goal: cv2.typing.Point,
  max_iterations: int = 10000,
  step_size: int = 10,
  verbose=False
) -> list:
  """
  Implements the Rapidly-Exploring Random Tree (RRT) algorithm.

  @param map: The map image with obstacles
  @param start: The start position
  @param goal: The goal position
  @param max_iterations: Maximum number of iterations for the RRT algorithm (default is 1000)
  @param step_size: The step size for tree expansion (default is 10)
  @param verbose: Whether or not to print verbose output (default is False)
  @return: The path found by the RRT algorithm
  """

  print("Executing RRT algorithm...")

  rrt_execution_time = 0
  rows, cols, rgb = map.shape
  nodes = [start]
  parent = {start: None}
  start_time = time.time()

  # TODO: Make more memory efficient, so we can increase max_iterations

  for i in range(max_iterations):
    # Random point in map
    rand_point = (random.randint(0, cols - 1), random.randint(0, rows - 1))
    # Find nearest node
    nearest_node = min(
      nodes,
      key=lambda node: np.linalg.norm(np.array(node) - np.array(rand_point))
    )
    # Steer towards the random point
    direction = np.array(rand_point) - np.array(nearest_node)
    length = np.linalg.norm(direction)

    if length == 0:
      continue

    direction = direction / length
    new_point = tuple((np.array(nearest_node) + step_size * direction).astype(int))

    # Check collision
    if (
      0 <= new_point[0] < cols
      and 0 <= new_point[1] < rows
      and isCollisionFree(map, nearest_node, new_point)
    ):
      nodes.append(new_point)
      parent[new_point] = nearest_node
      # Draw on map for visualization
      cv2.line(map, nearest_node, new_point, (0, 155, 255), 1) # Orange

      # Check if goal is reached
      if np.linalg.norm(np.array(new_point) - np.array(goal)) < step_size:
        cv2.line(map, new_point, goal, (0, 155, 255), 1) # Orange
        parent[goal] = new_point

        if verbose:
          
          print(f"Goal reached in {i} iterations!")

        # Record execution time
        end_time = time.time()
        rrt_execution_time = end_time - start_time
        break

  # Reconstruct path
  path = []

  if goal in parent:
    current = goal

    while current is not None:
      path.append(current)
      current = parent.pop((current[0], current[1]), parent[current])

    path.reverse()

    print("Alternative path found!")

    if verbose:
      print("Path length:", len(path))
    
  else:
    # Record execution time
    end_time = time.time()
    rrt_execution_time = end_time - start_time

    print("No path found!")

  print("RRT execution time:", round(rrt_execution_time, 6), "seconds")
  print()

  return path

