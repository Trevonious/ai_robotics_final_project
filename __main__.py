import sys
import time

sys.path.append('./ai_robotics_final_project')

from algorithms.d_star import executeDStar
from algorithms.rrt import executeRRT
from maps.generate_maps import *
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
d_star_path_color = (0, 0, 255) # Red
end_time = 0
map_solution_time = 0
start_time = 0
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
  d_star_map = map
  initial_rrt_map = map.copy()
  # D* algorithm
  start_time = time.time()
  d_star_solution_path = executeDStar(d_star_map, start, goal, verbose)
  # Record execution time
  end_time = time.time()
  map_solution_time = end_time - start_time

  if len(d_star_solution_path) != 0:
    drawPathPoints(d_star_map, d_star_solution_path, d_star_path_color, verbose)
    displayMap(d_star_map, "initial_solution", map_number, verbose)
    print()

    # RRT Algorithm
    start_time = time.time()
    rrt_solution_path = executeRRT(
      initial_rrt_map,
      start,
      goal,
      rrt_max_iterations,
      rrt_step_size,
      verbose
    )
    # Record execution time
    end_time = time.time()
    map_solution_time += end_time - start_time
    
    if len(rrt_solution_path) != 0:
      displayMap(initial_rrt_map, "rrt_initial_solution", map_number, verbose)
      print()
    else:
      saveMap(initial_rrt_map, "rrt_initial_failure", map_number, verbose)
      print("The RRT algorithm was unable to find a solution using the provided parameters.")
      print()

    # Dynamic Obstacle Simulation
    if len(d_star_solution_path) < math.floor(map_size * 0.05):
      
      print("D* path is too short to generate dynamic obstacles. Skipping dynamic obstacle simulation...")
      print()

    else:

      if num_dynamic_obstacles == math.floor(map_size * 0.005):

        if len(d_star_solution_path) < math.floor(map_size * 0.15):
          num_dynamic_obstacles = 1

          print("Path too short. Reduced number of dynamic obstacles to 1.")

        elif len(d_star_solution_path) < math.floor(map_size * 0.4):
          num_dynamic_obstacles = math.floor(num_dynamic_obstacles / 2)

          print(f"Path too short. Reduced number of dynamic obstacles to {num_dynamic_obstacles}.")
      
      print("Simulating dynamic obstacle(s)...")

      # Generate dynamic obstacles at selected point
      generateDynamicObstacle(
        d_star_map,
        d_star_solution_path,
        start,
        goal,
        num_dynamic_obstacles,
        verbose
      )

      if display_initial_maps:
        # Display the generated map with dynamic obstacles
        displayMap(d_star_map, "dynamic_obstacle", map_number, verbose)
      else:
        # Save the generated map with dynamic obstacles
        saveMap(d_star_map, "dynamic_obstacle", map_number, verbose)

      dynamic_obstacle_path = d_star_solution_path.copy()
      # D* Replanning Algorithm
      start_time = time.time()

      # TODO: Create function to backtrack solution path until collide with an
      # obstacle, then use RRT to get around the obstacle (reaching anywhere on
      # the path that is not already visited), updating the solution path, and
      # continue to the goal. Do this until:
      #   1. The goal is reached
      #   2. The path is blocked by another dynamic obstacle
      #   3. RRT is unable to find a path around an obstacle
      #
      # If you encounter the max number of dynamic obstacles for the map size
      # (math.floor(map_size * 0.005)) or if RRT is unable to find a path, rerun
      # the D* algorithm to find the new optimal path.
      #
      # When we have to rerun D*, we should save a picture of the map, then
      # remove the path from the diagram, repaint the start/goal points, and
      # then run D* again.

      # Record execution time
      end_time = time.time()
      map_solution_time += end_time - start_time
      
      if len(dynamic_obstacle_path) != 0:
        displayMap(d_star_map, "dynamic_obstacle_solution", map_number, verbose)
      else:
        print("There is no path between the start and goal points for this map.")
        print()

    if verbose:
      print(f"Map {map_number} Solution Time: {round(map_solution_time, 6)} seconds")
  else:
    print("There is no path between the start and goal points for this map.")
    print()
  
  total_execution_time += map_solution_time

  print(f"Execution completed for Map {map_number}!")
  print()

print("All maps have been processed!")
print(f"Total Execution Time - {map_number} Map(s): {round(total_execution_time, 6)} seconds")
print()
