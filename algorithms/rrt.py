import cv2
import numpy as np
import random
import sys
import time

sys.path.append('./ai_robotics_final_project')

from utils.points import isCollisionFree

def executeRRT(
  map: list,
  visited_path: list,
  unvisited_path: list,
  max_iterations: int = 10000,
  step_size: int = 10,
  verbose=False
) -> list:
  """
  Implements the Rapidly-Exploring Random Tree (RRT) algorithm.

  @param map: The map image with obstacles
  @param visited_path: The visited path
  @param unvisited_path: The unvisited path
  @param max_iterations: Maximum number of iterations for the RRT algorithm (default is 1000)
  @param step_size: The step size for tree expansion (default is 10)
  @param verbose: Whether or not to print verbose output (default is False)
  @return: The path found by the RRT algorithm
  """

  print("Executing RRT algorithm...")

  goal: tuple = None
  obstacle_color = "[0 0 0]"
  rrt_execution_time = 0
  rows, cols, rgb = map.shape
  # Get the start point for the RRT path
  start = visited_path.pop()
  rrt_visited = [ (start[0], start[1]) ]
  parent = { (start[0], start[1]): None }
  start_time = time.time()

  # TODO: Make more memory efficient, so we can increase max_iterations

  for i in range(max_iterations):
    # Random point in map
    rand_point = (random.randint(0, cols - 1), random.randint(0, rows - 1))
    # Find nearest node
    nearest_node = min(
      rrt_visited,
      key=lambda node: np.linalg.norm(np.array(node) - np.array(rand_point))
    )
    # Steer towards the random point
    direction = np.array(rand_point) - np.array(nearest_node)
    length = np.linalg.norm(direction)

    if length == 0:
      continue

    direction = direction / length
    new_point = tuple(
      (np.array(nearest_node) + step_size * direction).astype(int)
    )

    # Check collision
    if (
      0 <= new_point[0] < cols
      and 0 <= new_point[1] < rows
      and isCollisionFree(map, nearest_node, new_point, step_size)
    ):
      rrt_visited.append(new_point)
      parent[new_point] = nearest_node
      # Draw on map for visualization
      cv2.line(map, nearest_node, new_point, (0, 155, 255), 1) # Orange

      for unvisited_point in unvisited_path:
        
        # If unvisited_point is not an obstacle
        if str(map[(unvisited_point[1], unvisited_point[0])]) != obstacle_color:
          distance = np.linalg.norm(
            np.array(new_point) - np.array(unvisited_point)
          )
          
          # Check if a goal point is reached
          if distance < step_size:
            # Draw final 
            cv2.line(map, new_point, unvisited_point, (255, 155, 0), 1) # Light Blue
            parent[unvisited_point] = new_point
            # Record execution time
            end_time = time.time()
            rrt_execution_time = end_time - start_time
            goal = unvisited_point

            if verbose:
              print(f"Goal point ({str(goal[0])}, {str(goal[1])}) reached in {i} iterations!")

            break
    
    if goal:
      break
  
  path = []

  if goal:
    # Backtrack to get the path to goal point
    rrt_visited = [goal]
    current = parent.pop(goal, parent[goal])
    cv2.line(map, goal, current, (255, 155, 0), 1) # Light Blue

    while current is not None:
      rrt_visited.append(current)
      next = parent.pop(current, None)
      
      if next is not None:
        cv2.line(map, current, next, (255, 155, 0), 1) # Light Blue
        current = next
      elif current == start:
        current = None

    rrt_visited.reverse()
    visited_path.extend(rrt_visited)
    path = visited_path

    print("Alternative path found!")

    if verbose:
      print("Path length:", len(visited_path))
    
  else:
    # Record execution time
    end_time = time.time()
    rrt_execution_time = end_time - start_time
    path = []

    print("No path found!")

  print("RRT execution time:", round(rrt_execution_time, 6), "seconds")
  print()
  
  return path
