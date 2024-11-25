import sys
import time

sys.path.append('./ai_robotics_final_project')

from algorithms.rrt import executeRRT

def executeReplanning(
  map: list,
  path: list,
  threshold,
  verbose: bool = False
) -> list:
  """
  Execute the replanning algorithm by combining the D* and RRT algorithms.

  @param map: The map image with obstacles
  @param path: The path found by the D* algorithm
  @param threshold: The maximum number of obstacles to encounter before rerunning D*
  @param verbose: Whether or not to print verbose output (default is False)
  @return: The final path found by the replanning algorithm
  """

  print("Executing replanning algorithm...")

  # Obstacle color
  obstacle_color = "[0 0 0]"
  num_obstacles_encountered = 0
  # Traversing the path in reverse order
  d_star_path = path.copy()
  d_star_path.reverse()
  # Start becomes the goal
  goal = d_star_path[-1]

  if threshold <= 1:
    threshold = 1
  
  start_time = time.time()
  current = d_star_path.pop(0)
  visited = [current]

  # Iterate through the path
  while d_star_path:
    next = d_star_path.pop(0)

    if next == goal:
      visited.append(next)
      break
    elif num_obstacles_encountered > threshold:
      break

    if str(map[(next[1], next[0])]) == obstacle_color:

      if verbose:
        print(f"Obstacle detected at: ({next[0]}, {next[1]})")
      
      num_obstacles_encountered += 1
      # Use RRT to get around the obstacle
      # TODO: Change RRT to take a list for start and a list for goal
      #visited = executeRRT(map, visited, d_star_path, verbose)
      visited = []

      if visited:
        # Set last visited node as current
        current = visited[-1]
      else:
        # No path found
        break

      # Replan path around the obstacle
    else:
      visited.append(next)
      current = next

  # Reconstruct path
  replanned_path = visited

  if goal in replanned_path:
    end_time = time.time()
    replanning_execution_time = end_time - start_time
    replanned_path.reverse()

    print("Alternative path found!")

    if verbose:
      print("Replanned path length:", len(replanned_path))
    
  else:
    # Record execution time
    end_time = time.time()
    replanning_execution_time = end_time - start_time

    print("No path found!")

  print("Replanning execution time:", round(replanning_execution_time, 6), "seconds")
  print()

  return replanned_path
