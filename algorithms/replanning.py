import sys
import time

sys.path.append('./ai_robotics_final_project')

from algorithms.rrt import executeRRT

def executeReplanning(
  map: list,
  path: list,
  threshold,
  max_iterations,
  step_size,
  verbose: bool = False
) -> list:
  """
  Execute the replanning algorithm by combining the D* and RRT algorithms.

  @param map: The map image with obstacles
  @param path: The path found by the D* algorithm
  @param threshold: The maximum number of obstacles to encounter before rerunning D*
  @param max_iterations: Maximum number of iterations for the RRT algorithm
  @param step_size: The step size for tree expansion
  @param verbose: Whether or not to print verbose output (default is False)
  @return: The final path found by the replanning algorithm
  """

  print("Executing RRT replanning algorithm...")

  # Obstacle color
  obstacle_color = "[0 0 0]"
  num_obstacles_encountered = 0
  # Traversing the path in reverse order
  unvisited_d_star_path = path.copy()
  unvisited_d_star_path.reverse()
  # Start becomes the goal
  goal = unvisited_d_star_path[-1]

  if threshold <= 1:
    threshold = 1
  
  start_time = time.time()
  current = unvisited_d_star_path.pop(0)
  visited = [current]

  # Iterate through the path
  while len(unvisited_d_star_path) != 0:
    next = unvisited_d_star_path.pop(0)

    if next == goal:
      visited.append(next)
      break
    elif num_obstacles_encountered == threshold:
      
      if verbose:
        print(f"Number of obstacles encountered threshold ({threshold}) reached!")
      
      break

    if str(map[(next[1], next[0])]) == obstacle_color:

      if verbose:
        print(f"Obstacle detected at: ({next[0]}, {next[1]})")
      
      num_obstacles_encountered += 1
      # Use RRT to get around the obstacle
      replanned_path = executeRRT(
        map,
        visited,
        unvisited_d_star_path,
        max_iterations,
        step_size,
        verbose
      )

      if len(replanned_path) != 0:
        visited.extend(replanned_path)
        # Set last visited node as current
        current = visited[-1]
        unvisited_d_star_path = unvisited_d_star_path[
          unvisited_d_star_path.index(current) + 1:
        ]
      else:
        # No path found
        break

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
    replanned_path = []

    print("No path found!")

  print("RRT replanning execution time:", round(replanning_execution_time, 6), "seconds")
  print()

  return replanned_path
