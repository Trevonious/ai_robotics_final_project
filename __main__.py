import sys
import time

sys.path.append('./ai_robotics_final_project')

from algorithms.d_star import executeDStar
from algorithms.replanning import executeReplanning
from algorithms.rrt import executeRRT
from maps.generate_maps import *
from utils.args import parseArgs
from utils.points import clearPaths, drawPathPoints, selectInitialPoints

# See README.md for instructions on how to run this script.

# Parse command line arguments
args = parseArgs()
map_size = args.map_size
num_dynamic_obstacles = args.num_dynamic_obstacles
num_initial_obstacles = args.num_initial_obstacles
num_maps = args.num_maps
rrt_max_iterations = args.rrt_max_iterations
rrt_step_size = args.rrt_step_size
replanning_threshold = args.replanning_threshold
verbose = args.verbose

# Main execution
d_star_dynamic_obstacle_path_length = 0
d_star_dynamic_obstacle_time = 0
d_star_initial_path_length = 0
d_star_initial_time = 0
d_star_path_color = (0, 0, 255) # Red
end_time = 0
map_solution_time = 0
replanning_path_color = (255, 0, 255) # Purple
rrt_initial_path_length = 0
rrt_initial_time = 0
rrt_replanning_path_length = 0
rrt_replanning_time = 0
start_time = 0
total_execution_time = 0
map_number = 0
maps = generateMaps(
  map_size,
  num_maps,
  num_initial_obstacles,
  verbose
)

for map in maps:
  replanning_map = None
  map_number += 1
  start, goal = selectInitialPoints(map, verbose)
  # D* algorithm
  start_time = time.time()
  d_star_initial_solution_path = executeDStar(map, start, goal, verbose)
  # Record execution time
  end_time = time.time()
  d_star_initial_time = end_time - start_time
  map_solution_time = d_star_initial_time
  d_star_initial_path_length = len(d_star_initial_solution_path)

  if d_star_initial_path_length != 0:
    drawPathPoints(map, d_star_initial_solution_path, d_star_path_color, verbose)
    displayMap(map, "d*_initial_solution", map_number, verbose)

    print()
    
    rrt_initial_solution_path = [start]
    # RRT Algorithm
    start_time = time.time()
    rrt_initial_solution_path = executeRRT(
      map,
      rrt_initial_solution_path,
      [goal],
      rrt_max_iterations,
      rrt_step_size,
      verbose
    )
    # Record execution time
    end_time = time.time()
    rrt_initial_time = end_time - start_time
    map_solution_time += rrt_initial_time
    rrt_initial_path_length = len(rrt_initial_solution_path)
    
    if rrt_initial_path_length != 0:
      drawPathPoints(map, d_star_initial_solution_path, d_star_path_color, verbose)
      displayMap(map, "rrt_initial_solution", map_number, verbose)

      print()

    else:
      saveMap(map, "rrt_initial_failure", map_number, verbose)

      print("The RRT algorithm was unable to find a solution using the provided parameters.")
      print()

    # Clear paths from the map
    clearPaths(map, start, goal, verbose)
    # Redraw D* solution path
    drawPathPoints(map, d_star_initial_solution_path, d_star_path_color, verbose)

    # Dynamic Obstacle Simulation
    if len(d_star_initial_solution_path) < math.floor(map_size * 0.05):
      print("D* path is too short to generate dynamic obstacles. Skipping dynamic obstacle simulation...")
      print()

    else:

      if num_dynamic_obstacles == math.floor(map_size * 0.005):

        if len(d_star_initial_solution_path) < math.floor(map_size * 0.15):
          num_dynamic_obstacles = 1

          print("Path too short. Reduced number of dynamic obstacles to 1.")

        elif len(d_star_initial_solution_path) < math.floor(map_size * 0.4):
          num_dynamic_obstacles = math.floor(num_dynamic_obstacles / 2)

          print(f"Path too short. Reduced number of dynamic obstacles to {num_dynamic_obstacles}.")
      
      print("Simulating dynamic obstacle(s)...")

      # Generate dynamic obstacles at selected point
      generateDynamicObstacle(
        map,
        d_star_initial_solution_path,
        start,
        goal,
        num_dynamic_obstacles,
        verbose
      )
      # Save the generated map with dynamic obstacles
      saveMap(map, "dynamic_obstacle", map_number, verbose)

      print()

      # Clear paths from the map
      clearPaths(map, start, goal, verbose)
      # Replanning Algorithm
      start_time = time.time()
      rrt_replanning_solution_path = executeReplanning(
        map,
        d_star_initial_solution_path,
        replanning_threshold,
        rrt_max_iterations,
        rrt_step_size,
        verbose
      )
      # Record execution time
      end_time = time.time()
      rrt_replanning_time = end_time - start_time
      map_solution_time += rrt_replanning_time
      rrt_replanning_path_length = len(rrt_replanning_solution_path)
      
      if rrt_replanning_path_length != 0:
        drawPathPoints(map, d_star_initial_solution_path, d_star_path_color, verbose)
        displayMap(map, "rrt_replanning_solution", map_number, verbose)
        
        clearPaths(map, start, goal, verbose)
        
        replanning_map = map.copy()
        
        drawPathPoints(replanning_map, rrt_replanning_solution_path, replanning_path_color, verbose)
        displayMap(replanning_map, "replanning_only_solution", map_number, verbose)
        
        print()

      else:
        saveMap(map, "rrt_replanning_failure", map_number, verbose)

        print("RRT Replanning failed.")
        print()

      # Clear paths from the map
      clearPaths(map, start, goal, verbose)

      print("Rerunning D* algorithm...")

      start_time = time.time()
      # Execute D* algorithm with original start and goal
      d_star_dynamic_obstacle_solution_path = executeDStar(
        map,
        start,
        goal,
        verbose
      )
      # Record execution time
      end_time = time.time()
      d_star_dynamic_obstacle_time = end_time - start_time
      map_solution_time += d_star_dynamic_obstacle_time
      d_star_dynamic_obstacle_path_length = len(
        d_star_dynamic_obstacle_solution_path
      )

      if d_star_dynamic_obstacle_path_length != 0:
        drawPathPoints(
          map,
          d_star_dynamic_obstacle_solution_path,
          d_star_path_color,
          verbose
        )
        displayMap(map, "d*_dynamic_obstacle_solution", map_number, verbose)
        
        print()
        
        if replanning_map is not None:
          drawPathPoints(
            replanning_map,
            d_star_dynamic_obstacle_solution_path,
            d_star_path_color,
            verbose
          )
          displayMap(replanning_map, "d*_and_rrt_replanning_solution", map_number, verbose)

        print()

      else:
        print("There is no path between the start and goal points for the dynamic obstacle map.")
        print()
    
  else:
    print("There is no path between the start and goal points for this map.")
    print()
  
  total_execution_time += map_solution_time

  if verbose:

    if d_star_initial_time != 0:
      
      if d_star_initial_path_length != 0:
        print(f"D* Initial Solution Path Length: {d_star_initial_path_length}")
      else:
        print("No D* initial solution path found.")
      
      print(f"D* Initial Execution Time: {round(d_star_initial_time, 6)} seconds")

    if rrt_initial_time != 0:
      
      if rrt_initial_path_length != 0:
        print(f"RRT Initial Solution Path Length: {rrt_initial_path_length} (RRT step size = {rrt_step_size})")
      else:
        print("No RRT initial solution path found.")
      
      print(f"RRT Initial Execution Time: {round(rrt_initial_time, 6)} seconds")

    if rrt_replanning_time != 0:
      
      if rrt_replanning_path_length != 0:
        print(f"RRT Replanning Solution Path Length: {rrt_replanning_path_length} (RRT step size = {rrt_step_size})")
      else:
        print("No RRT replanning solution path found.")
      
      print(f"RRT Replanning Execution Time: {round(rrt_replanning_time, 6)} seconds")

    if d_star_dynamic_obstacle_time != 0:
      
      if d_star_dynamic_obstacle_path_length != 0:
        print(f"D* Dynamic Obstacle Solution Path Length: {d_star_dynamic_obstacle_path_length}")
      else:
        print("No D* dynamic obstacle solution path found.")
      
      print(f"D* Dynamic Obstacle Execution Time: {round(d_star_dynamic_obstacle_time, 6)} seconds")
      
    print(f"Map {map_number} Solution Time: {round(map_solution_time, 6)} seconds")

  print(f"Execution completed for Map {map_number}!")
  print()

print("All maps have been processed!")
print(f"Total Execution Time - {map_number} Map(s): {round(total_execution_time, 6)} seconds")
print()
