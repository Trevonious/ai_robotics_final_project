import argparse
import sys

sys.path.append('./../map')

from generate_maps import generateMaps

# To run this script, use the following command:
#   py test_generate_maps.py
#
# To pass in parameters, use the following flags:
#   -d or --display: Display generated maps, one by one
#   -nm or --num_maps: The number of maps to generate
#   -no or --num_obstacles: The number of obstacles to generate
#   -v or --verbose: Verbose output
#
# Example of using flags:
#   py test_generate_maps.py -d True -nm 5 -no 10 -v True

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--display', help='Display generated maps, one by one', type=bool, default=False)
parser.add_argument('-nm', '--num_maps', help='The number of maps to generate', type=int, default=1)
parser.add_argument('-no', '--num_obstacles', help='The number of obstacles to generate', type=int, default=20)
parser.add_argument('-tr', '--test_run', help='Whether or not this is a test run', type=bool, default=False)
parser.add_argument('-v', '--verbose', help='Verbose output', type=bool, default=False)
args = parser.parse_args()

generateMaps(args.display, args.num_maps, args.num_obstacles, args.verbose)