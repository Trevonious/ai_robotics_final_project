import sys
import time

sys.path.append('./ai_robotics_final_project')

from d_star.d_star import *
from map.generate_maps import *
from rrt.rrt import rrt
from utils.args import parseArgs
from utils.points import drawPathPoints, selectInitialPoints

# See README.md for instructions on how to run this script.

# Parse command line arguments
args = parseArgs()
display_initial_maps = args.display_initial_maps
map_size = args.map_size
num_dynamic_obstacles = args.num_dynamic_obstacles
num_initial_obstacles = args.num_initial_obstacles
num_maps = args.num_maps
rrt_max_iterations = args.rrt_max_iterations
rrt_step_size = args.rrt_step_size
verbose = args.verbose

# Main execution
d_star_color = (0, 0, 255) # Red
rrt_color = (0, 255, 255) # Yellow
start_time = time.time()
total_execution_time = 0
map_number = 0
maps = generateMaps(
  display_initial_maps,
  map_size,
  num_maps,
  num_initial_obstacles,
  verbose
)

for map in maps:
  map_number += 1
  start, goal = selectInitialPoints(map, verbose)
  path = dStar(map, start, goal, verbose)
  # Record execution time
  end_time = time.time()
  map_solution_time = end_time - start_time

  if len(path) != 0:
    drawPathPoints(map, path, d_star_color, verbose)
    displayMap(map, "initial_solution", map_number, verbose)

    if len(path) < math.floor(map_size * 0.05):
      
      print("Path too short to generate dynamic obstacles. Skipping dynamic obstacle simulation...")

    else:

      if num_dynamic_obstacles == math.floor(map_size * 0.005):

        if len(path) < math.floor(map_size * 0.15):
          num_dynamic_obstacles = 1

          print("Path too short. Reduced number of dynamic obstacles to 1.")

        elif len(path) < math.floor(map_size * 0.4):
          num_dynamic_obstacles = math.floor(num_dynamic_obstacles / 2)

          print(f"Path too short. Reduced number of dynamic obstacles to {num_dynamic_obstacles}.")
      
      print("Simulating dynamic obstacle(s)...")

      # Generate dynamic obstacles at selected point
      generateDynamicObstacle(
        map,
        path,
        start,
        goal,
        num_dynamic_obstacles,
        verbose
      )

      # Display the generated map with dynamic obstacles
      displayMap(map, "dynamic_obstacle", map_number, verbose)

      print("Executing RRT...")

      start_time = time.time()

      rrt_path = rrt(
        map,
        start,
        goal,
        rrt_max_iterations,
        rrt_step_size,
        verbose
      )
      # Record execution time
      end_time = time.time()
      map_solution_time += end_time - start_time
      
      if len(rrt_path) != 0:
        #drawPathPoints(map, rrt_path, rrt_color, verbose)
        displayMap(map, "dynamic_obstacle_solution", map_number, verbose)
      else:
        print("There is no path between the start and goal points for this map.")

    if verbose:
      print(f"Map {map_number} Solution Time: {round(map_solution_time, 6)} seconds")
  else:
    print("There is no path between the start and goal points for this map.")
  
  total_execution_time += map_solution_time

  print(f"Execution completed for Map {map_number}!")

print(f"Total Execution Time - {map_number} Map(s): {round(total_execution_time, 6)} seconds")
