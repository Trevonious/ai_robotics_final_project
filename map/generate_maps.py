import sys
import cv2
import glob
import math
import numpy as np
import os
import random
import time

def generateMaps(
  display_maps = False,
  number_maps = 1,
  number_obstacles = 20,
  test_run = False,
  verbose = False
) -> list:
  """
  Generate maps with random obstacles and save them as images in the 
  <i>map/images</i> folder.

  @param display_maps: Display generated maps, one by one (default is False)
  @param number_maps: The number of maps to generate (default is 1)
  @param number_obstacles: The number of obstacles to generate (default is 20)
  @param test_run: Whether or not this is a test run (default is False)
  @param verbose: Verbose output (default is False)
  @return: A list of generated maps
  """

  print("Generating maps...")

  start_time = time.time()
  images_folder_path = './ai_robotics_final_project/map/images/'

  if test_run:
    images_folder_path = './ai_robotics_final_project/tests/images/'

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
      generateObstacle(map)

    if should_display_maps:
      # Display the image
      cv2.imshow("Map " + map_number, map)
      cv2.waitKey(0)
      cv2.destroyAllWindows()

    # Save the image
    cv2.imwrite(images_folder_path + "map" + map_number + ".png", map)
    maps.append(np.array(map))
  
  end_time = time.time()
  total_map_generation_time = end_time - start_time

  print(str(verbose))

  if verbose:
    print("Total Map Generation Time:", total_map_generation_time, "seconds")
  
  print("Maps generated successfully!")
  
  return maps

def generateObstacle(map, x_coord = -1, y_coord = -1) -> None:
  """
  Randomly obstacle on the map, if x_coord and y_coord are no provided,
  otherwise generate an obstacle at the specified coordinates.

  @param map: The map to generate the obstacle on
  @param x_coord: The x-coordinate of the obstacle (default is -1)
  @param y_coord: The y-coordinate of the obstacle (default is -1)
  """

  x = x_coord
  y = y_coord

  if x_coord == -1 or y_coord == -1:
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
