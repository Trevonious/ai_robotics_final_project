import argparse
from generate_maps import generateMaps

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--display', help='Display generated maps, one by one', type=bool, default=False)
parser.add_argument('-nm', '--num_maps', help='The number of maps to generate', type=int, default=1)
parser.add_argument('-no', '--num_obstacles', help='The number of obstacles to generate', type=int, default=20)
args = parser.parse_args()

generateMaps(args.num_maps, args.num_obstacles, args.display)