import argparse
import cv2
import os
import sys
import time
import numpy as np

sys.path.append('./ai_robotics_final_project')

from d_star.d_star import dStar, selectPoints
from RRT.rrt import RRT  # Ensure RRT logic is in rrt.py under rrt module
from map.generate_maps import generateMaps

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-nm', '--num_maps', help='The number of maps to generate', type=int, default=1)
parser.add_argument('-no', '--num_obstacles', help='The number of obstacles to generate', type=int, default=20)
parser.add_argument('-tr', '--test_run', help='Whether or not this is a test run', type=bool, default=False)
parser.add_argument('-v', '--verbose', help='Verbose output', type=bool, default=False)
parser.add_argument('-d', '--display', help='Display generated maps one by one', type=bool, default=False)
args = parser.parse_args()

# Main execution
solutions_folder_path = './ai_robotics_final_project/map/images/solutions/'
map_number = 1
maps = generateMaps(
    display_maps=args.display,
    number_maps=args.num_maps,
    number_obstacles=args.num_obstacles,
    test_run=args.test_run,
    verbose=args.verbose
)

for map in maps:
    print(f"Processing Map {map_number}...")

    # Ensure the map is grayscale (RRT requires a 2D array)
    if len(map.shape) == 3:  # Check if the map has 3 channels (color image)
        grayscale_map = cv2.cvtColor(map, cv2.COLOR_BGR2GRAY)
    else:
        grayscale_map = map.copy()

    # Convert the map to BGR format for D* (requires 3D input)
    dstar_map_input = cv2.cvtColor(grayscale_map, cv2.COLOR_GRAY2BGR)

    # Select start and goal points
    start, goal = selectPoints(grayscale_map, args.verbose)

    # Execute D* algorithm
    print("Executing D* algorithm...")
    dstar_start_time = time.time()
    dstar_path = dStar(dstar_map_input.copy(), start, goal, args.verbose)
    dstar_time = time.time() - dstar_start_time
    print(f"D* completed in {dstar_time:.2f} seconds.")

    # Visualize D* path
    dstar_map = dstar_map_input.copy()
    for point in dstar_path:
        dstar_map[point[1], point[0]] = (0, 0, 255)  # Path in red
    cv2.imwrite(solutions_folder_path + f"map{map_number}_dstar_solution.png", dstar_map)

    # Execute RRT algorithm
    print("Executing RRT algorithm...")
    rrt_start_time = time.time()
    rrt_path = RRT(grayscale_map.copy(), start, goal, verbose=args.verbose)
    rrt_time = time.time() - rrt_start_time
    print(f"RRT completed in {rrt_time:.2f} seconds.")

    # Visualize RRT path
    rrt_map = cv2.cvtColor(grayscale_map.copy(), cv2.COLOR_GRAY2BGR)  # Convert back to color for visualization
    for point in rrt_path:
        rrt_map[point[1], point[0]] = (0, 255, 0)  # Path in green
    cv2.imwrite(solutions_folder_path + f"map{map_number}_rrt_solution.png", rrt_map)

    # Always display visualization
    cv2.imshow(f'Map {map_number} - D* Path', dstar_map)
    cv2.imshow(f'Map {map_number} - RRT Path', rrt_map)
    print("Press any key to continue to the next map...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Print time comparison
    print(f"Time Comparison for Map {map_number}:")
    print(f"  D*:  {dstar_time:.2f} seconds")
    print(f"  RRT: {rrt_time:.2f} seconds")

    map_number += 1

print("Processing complete.")
