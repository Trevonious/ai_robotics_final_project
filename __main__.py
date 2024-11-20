import argparse
import cv2
import sys
import time

sys.path.append('./ai_robotics_final_project')

from d_star.d_star import *
from map.generate_maps import generateMaps

# See README.md for instructions on how to run this script.

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--display', help='Display generated maps, one by one', type=bool, default=False)
parser.add_argument('-nm', '--num_maps', help='The number of maps to generate', type=int, default=1)
parser.add_argument('-no', '--num_obstacles', help='The number of obstacles to generate', type=int, default=20)
parser.add_argument('-tr', '--test_run', help='Whether or not this is a test run', type=bool, default=False)
parser.add_argument('-v', '--verbose', help='Verbose output', type=bool, default=False)
args = parser.parse_args()

# Main execution
start_time = time.time()
solutions_folder_path = './ai_robotics_final_project/map/images/solutions/'
map_number = 1
maps = generateMaps(
  args.display,
  args.num_maps,
  args.num_obstacles,
  args.test_run,
  args.verbose
)

for map in maps:

  print("Executing D* algorithm on Map", map_number, "...")

  start, goal = selectPoints(map, args.verbose)
  path = dStar(map, start, goal, args.verbose)

  print("Drawing path (red) on map...")

  # Visualize
  for point in path:
    map[(point[1], point[0])] = (0, 0, 255)  # Path in red

  end_time = time.time()
  total_execution_time = end_time - start_time

  if (args.verbose):
    print(f"Total Execution Time: {total_execution_time} seconds")
  
  cv2.imshow('Path', map)
  cv2.waitKey(0)
  cv2.imwrite(solutions_folder_path + "map" + str(map_number) + "_solution.png", map)
  cv2.destroyAllWindows()

  print("Algorithm complete for Map", map_number, "!")

  map_number += 1
