import argparse
import cv2
import glob
import math
import numpy as np
import os
import random

# To run this script, use the following command:
#   py generate_maps.py
#
# To pass in parameters, use the following flags:
#   -d or --display: Display generated maps, one by one
#   -nm or --num_maps: The number of maps to generate
#   -no or --num_obstacles: The number of obstacles to generate
#
# Example:
#   py generate_maps.py -d True -nm 5 -no 10

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--display', help='Display generated maps, one by one', type=bool, default=False)
parser.add_argument('-nm', '--num_maps', help='The number of maps to generate', type=int, default=1)
parser.add_argument('-no', '--num_obstacles', help='The number of obstacles to generate', type=int, default=20)
args = parser.parse_args()


def generateMaps(number_maps = 1, number_obstacles = 20, display_maps = False):
  """
  Generate maps with random obstacles and save them as images in the 
  <i>map/images</i> folder.

  @param number_maps: The number of maps to generate (default is 1)
  @param number_obstacles: The number of obstacles to generate (default is 20)
  @param display_maps: Display generated maps, one by one (default is False)

  Returns:
    An array of generated maps
  """

  images_folder_path = './map/images/'
  maps = []
  num_maps = number_maps
  num_obstacles = number_obstacles
  should_display_maps = display_maps

  # Get list of files in the images folder
  files = glob.glob(images_folder_path + '*.png')

  # Delete all files in the images folder
  for f in files:
    os.remove(f)

  # Generate maps
  for i in range(num_maps):
    # Create a blank image
    map = np.zeros((400, 400, 3), np.uint8)
    map[:] = (255, 255, 255)  # White background
    map_number = str(i + 1)

    # Generate random obstacles
    for i in range(num_obstacles):
      # Randomly generate coordinates
      x = random.randint(50, 350)
      y = random.randint(50, 350)

      radius = random.randint(10, 50)
      color = (0, 0, 0)
      # circle = 0, ellipse = 1, triangle = 2, rectangle/square = 3
      shape = random.randint(0, 3)

      if shape == 0:
        # Draw a circle
        orientation_x = random.randint(0, 2)
        orientation_y = random.randint(0, 2)

        if orientation_x == 1:
          x = x - math.floor(radius / 2)
        elif orientation_x == 2:
          x = x + math.floor(radius / 2)

        if orientation_y == 1:
          y = y + math.floor(radius / 2)
        elif orientation_y == 2:
          y = y - math.floor(radius / 2)

        cv2.circle(map, (x, y), radius, color, -1)
      elif shape == 1:
        # Draw an ellipse
        axes_height = random.randint(10, 50)
        axes_width = random.randint(10, 50)
        orientation_x = random.randint(0, 2)
        orientation_y = random.randint(0, 2)

        if orientation_x == 1:
          x = x - math.floor(axes_width / 2)
        elif orientation_x == 2:
          x = x + math.floor(axes_width / 2)

        if orientation_y == 1:
          y = y + math.floor(axes_height / 2)
        elif orientation_y == 2:
          y = y - math.floor(axes_height / 2)
        
        cv2.ellipse(map, (x, y), (axes_width, axes_height), 0, 0, 360, color, -1)
      elif shape == 2:
        # Draw a triangle
        points = np.array(
          [
            [x, y],
            [x + radius, y],
            [x + radius / 2, y - radius]
          ],
          np.int32
        )
        points = points.reshape((-1, 1, 2))
        cv2.fillPoly(map, [points], color)
      elif shape == 3:
        # Draw a rectangle
        orientation_x = random.randint(0, 1)
        orientation_y = random.randint(0, 1)
        size_x = radius * random.randint(1, 3)
        size_y = radius * random.randint(1, 3)
        x2 = x + size_x
        y2 = y - size_y

        if orientation_x == 0:
          x2 = x - size_x

        if orientation_y == 0:
          y2 = y + size_y
        
        cv2.rectangle(map, (x, y), (x2, y2), color, -1)

    if should_display_maps:
      # Display the image
      cv2.imshow("Map " + map_number, map)
      cv2.waitKey(0)
      cv2.destroyAllWindows()

    # Save the image
    cv2.imwrite(images_folder_path + "map" + map_number + ".png", map)
    maps.append(map)
  
  return maps

generateMaps(args.num_maps, args.num_obstacles, args.display)
