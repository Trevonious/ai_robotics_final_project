import argparse
import math

def parseArgs() -> argparse.Namespace:
  """
  Parse and validate command line arguments.

  @return: The parsed and validated command line arguments.
  """
  
  # Parse command line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-ms', '--map_size', help='The length and width of the map, in pixels (min=100; max=1000)', type=int, default=800)
  parser.add_argument('-ndo', '--num_dynamic_obstacles', help='The number of dynamic obstacles to generate on the solution path (min=1; max=0.5%% of map_size)', type=int, default=4)
  parser.add_argument('-nio', '--num_initial_obstacles', help='The number of initial obstacles to generate (min=1; max=5%% of map_size)', type=int, default=40)
  parser.add_argument('-nm', '--num_maps', help='The number of maps to generate', type=int, default=1)
  parser.add_argument('-rmi', '--rrt_max_iterations', help='The maximum iterations for the RRT algorithm (min=1,000; max=8,000)', type=int, default=4000)
  parser.add_argument('-rss', '--rrt_step_size', help='The step size for the RRT algorithm (min=1; max=1%% of map_size)', type=int, default=8)
  parser.add_argument('-rt', '--replanning_threshold', help='The replanning encountered obstacle threshold for the D* algorithm (min=1; max=0.5%% of map_size)', type=int, default=4)
  parser.add_argument('-v', '--verbose', help='Whether or not to print more detailed output in the console', type=bool, default=False)
  args = parser.parse_args()
  # Validate args and adjust, if necessary
  validateArgs(args)

  return args

def validateArgs(args: argparse.Namespace) -> None:
  """
  Validate the command line arguments, adjusting them if necessary.

  @param args: The command line arguments to validate.
  """

  print()
  print("Validating arguments...")
  
  if args.map_size < 100:
    args.map_size = 100

    print("Map size is too small. Using minimum value of 100.")

  elif args.map_size > 1000:
    args.map_size = 1000

    print("Map size is too large. Using maximum value of 1000.")

  if args.num_dynamic_obstacles < 1:
    args.num_dynamic_obstacles = 1

    print("Number of dynamic obstacles is too small. Using minimum value of 1.")

  elif args.num_dynamic_obstacles > args.map_size * 0.005:
    num_dynamic_obstacles = math.floor(args.map_size * 0.005)
    args.num_dynamic_obstacles = num_dynamic_obstacles

    if args.num_dynamic_obstacles < 1:
      args.num_dynamic_obstacles = 1

      print("Number of dynamic obstacles is too small. Using minimum value of 1.")
    else:
      print("Number of dynamic obstacles is too large. Using maximum value of 0.5%% of map size (" + str(num_dynamic_obstacles) + ").")

  if args.num_initial_obstacles < 1:
    args.num_initial_obstacles = 1

    print("Number of initial obstacles is too small. Using minimum value of 1.")

  elif args.num_initial_obstacles > args.map_size * 0.05:
    num_initial_obstacles = math.floor(args.map_size * 0.05)
    args.num_initial_obstacles = num_initial_obstacles

    print("Number of initial obstacles is too large. Using maximum value of 5%% of map size (" + str(num_initial_obstacles) + ").")

  if args.rrt_max_iterations < 1000:
    args.rrt_max_iterations = 1000

    print("RRT max iterations is too small. Using minimum value of 1000.")

  elif args.rrt_max_iterations > 8000:
    rrt_max_iterations = 8000
    args.rrt_max_iterations = rrt_max_iterations

    print("RRT max iterations is too large. Using maximum value of 8,000.")

  if args.rrt_step_size < 1:
    args.rrt_step_size = 1

    print("RRT step size is too small. Using minimum value of 1.")

  elif args.rrt_step_size > args.map_size * 0.01:
    rrt_step_size = math.floor(args.map_size * 0.01)
    args.rrt_step_size = rrt_step_size

    print("RRT step size is too large. Using maximum value of 1%% of map size (" + str(rrt_step_size) + ").")

  if args.replanning_threshold < 1:
    args.replanning_threshold = 1

    print("Replanning threshold is too small. Using minimum value of 1.")

  elif args.replanning_threshold > args.map_size * 0.005:
    replanning_threshold = math.floor(args.map_size * 0.005)
    args.replanning_threshold = replanning_threshold

    if args.replanning_threshold < 1:
      args.replanning_threshold = 1

      print("Replanning threshold is too small. Using minimum value of 1.")
    else:
      print("Replanning threshold is too large. Using maximum value of 0.5%% of map size (" + str(replanning_threshold) + ").")

  print("Arguments validated successfully!")
  print()
