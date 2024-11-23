import cv2
import math
import numpy as np
import random
import sys
import time

sys.path.append('./ai_robotics_final_project')

from utils.files import deleteImages
from utils.points import drawInitialPoints, drawPathPoints, selectPathPoint
from utils.strings import getFormattedMapTitle

def generateMaps(
  display_initial_maps: bool = False,
  map_size: int = 400,
  number_maps: int = 1,
  number_obstacles: int = 20,
  verbose: bool = False
) -> list:
  """
  Generates maps with random obstacles and saves them as images in the 
  <i>map/images/initial</i> folder.

  @param display_initial_maps: Whether or not to display the initial generated maps, one by one (default is False)
  @param map_size: The size of the map (default is 400)
  @param number_maps: The number of maps to generate (default is 1)
  @param number_obstacles: The number of obstacles to generate (default is 20)
  @param verbose: Whether or not to print verbose output (default is False)
  @return: A list of generated maps
  """

  # Delete images from previous run
  deleteImages(verbose)

  print("Generating maps...")

  start_time = time.time()
  maps = []
  num_maps = number_maps
  num_obstacles = number_obstacles
  should_display_maps = display_initial_maps
  suffix = "initial"

  # Generate maps
  for i in range(num_maps):
    # Create a blank image
    map = np.zeros((map_size, map_size, 3), np.uint8)
    map[:] = (255, 255, 255)  # White background
    map_number = str(i + 1)

    # Generate random obstacles
    for i in range(num_obstacles):
      generateObstacle(map)

    if should_display_maps:
      displayMap(map, suffix, map_number, verbose)
    else:
      saveMap(map, suffix, map_number, verbose)
    
    maps.append(np.array(map))

    if verbose:
      print(f"Map {map_number} generated successfully!")
  
  # Record execution time
  end_time = time.time()
  total_map_generation_time = end_time - start_time

  if verbose:
    print(f"Total Map Generation Time: {round(total_map_generation_time, 6)} seconds")
  
  print("Maps generated successfully!")
  print()
  
  return maps

def generateObstacle(map: list, x_coord: int = -1, y_coord: int = -1) -> None:
  """
  Randomly place an obstacle on the map, if x_coord and y_coord are no provided,
  otherwise generate an obstacle at the specified coordinates.

  @param map: The map to generate the obstacle on
  @param x_coord: The x-coordinate of the obstacle (default is -1)
  @param y_coord: The y-coordinate of the obstacle (default is -1)
  """

  # Set obstacle color to black
  color = (0, 0, 0)
  map_size = map.shape[0]
  max_obstacle_radius_percentage = 0.1

  # If x_coord and y_coord are provided, set the percentage to 5%, so that
  # resulting obstacle is smaller and less likely to block start and goal points
  if x_coord != -1 and y_coord != -1:
    max_obstacle_radius_percentage = 0.05
  
  max_obstacle_radius = math.floor(map_size * max_obstacle_radius_percentage)
  min_obstacle_radius = math.floor(max_obstacle_radius * 0.2)
  radius = random.randint(min_obstacle_radius, max_obstacle_radius)
  x = x_coord
  y = y_coord

  # If x_coord and y_coord are not provided, generate random coordinates
  if x_coord == -1 or y_coord == -1:
    # Randomly generate coordinates
    x = random.randint(max_obstacle_radius, map_size - max_obstacle_radius)
    y = random.randint(max_obstacle_radius, map_size - max_obstacle_radius)

  # circle = 0, ellipse = 1, triangle = 2, rectangle/square = 3
  shape = random.randint(0, 3)

  if shape == 0: # Draw a circle
    
    if x_coord == -1 and y_coord == -1:
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
  elif shape == 1: # Draw an ellipse
    axes_height = random.randint(min_obstacle_radius, max_obstacle_radius)
    axes_width = random.randint(min_obstacle_radius, max_obstacle_radius)
    
    if x_coord == -1 and y_coord == -1:
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
  elif shape == 2: # Draw a triangle
    points = np.array(
      [
        [x - math.floor(radius / 2), y],
        [x + math.floor(radius / 2), y],
        [x, y - radius]
      ],
      np.int32
    )
    points = points.reshape((-1, 1, 2))
    cv2.fillPoly(map, [points], color)
  elif shape == 3: # Draw a rectangle
    size_multiplier_x = random.randint(1, 3)
    size_multiplier_y = random.randint(1, 3)

    if x_coord != -1 and y_coord != -1:
      size_multiplier_x = random.randint(1, 2)
      size_multiplier_y = random.randint(1, 2)

    size_x = math.floor(radius * size_multiplier_x / 2)
    size_y = math.floor(radius * size_multiplier_y / 2)
    x = x - size_x
    y = y - size_y
    x2 = x + size_x
    y2 = y + size_y

    if x_coord == -1 and y_coord == -1:
      orientation_x = random.randint(0, 1)
      orientation_y = random.randint(0, 1)

      if orientation_x == 0:
        x2 = x - size_x

      if orientation_y == 0:
        y2 = y + size_y

    cv2.rectangle(map, (x, y), (x2, y2), color, -1)

def displayMap(
  map: list,
  filename_suffix: str,
  number: int,
  verbose: bool = False
) -> None:
  """
  Display and save the provided map.

  @param map: The map to display
  @param filename_suffix: The filename suffix for the map
  @param number: The number of the map
  @param verbose: Whether or not to print verbose output (default is False)
  """

  title = getFormattedMapTitle(filename_suffix, number)

  if verbose:
    print(f"Displaying {title}...")

  cv2.imshow(title, map)
  cv2.waitKey(0)
  saveMap(map, filename_suffix, number, verbose)
  cv2.destroyAllWindows()

def saveMap(
  map: list,
  filename_suffix: str,
  number: int,
  verbose: bool = False
) -> None:
  """
  Save the provided map, as a PNG image.

  @param map: The map to save
  @param filename_suffix: The filename suffix for the map
  @param number: The number of the map
  @param verbose: Whether or not to print verbose output (default is False)
  """

  title = getFormattedMapTitle(filename_suffix, number)

  if verbose:
    print(f"Saving {title}...")

  images_folder_path = './ai_robotics_final_project/maps/images/'
  map_filename = "map" + str(number)

  if filename_suffix != "":
    images_folder_path += filename_suffix + '/'
    map_filename += "_" + filename_suffix
  
  map_filename += ".png"

  cv2.imwrite(images_folder_path + map_filename, map)

  if verbose:
    print(title + " saved successfully!")

def generateDynamicObstacle(
  map: list,
  path: list,
  start: cv2.typing.Point,
  goal: cv2.typing.Point,
  num_dynamic_obstacles: int,
  verbose: bool = False
) -> None:
  """
  Generate a dynamic obstacle on the map at the specified coordinates.

  @param map: The map to generate the dynamic obstacle on
  @param path: The path to select a point from
  @param start: The start point
  @param goal: The goal point
  @param num_dynamic_obstacles: The number of dynamic obstacles to generate
  @param verbose: Whether or not to print verbose output (default is False)
  """

  original_path_length = len(path)
  path_color = (0, 0, 255)
  path_covered = path.copy()
  path_points_covered = 0

  print(f"Generating {num_dynamic_obstacles} dynamic obstacles...")

  for i in range(num_dynamic_obstacles):
    obstacle_number = i + 1
    # Select a random point along the path
    dynamicObstacleCoords = selectPathPoint(path_covered, verbose)

    if verbose:
      print(f"Generating dynamic obstacle {obstacle_number}...")

    # Generate a dynamic obstacle
    generateObstacle(map, dynamicObstacleCoords[0], dynamicObstacleCoords[1])

    if verbose:
      print(f"Dynamic obstacle {obstacle_number} generated successfully!")
    
    # Get all points that are part of the path (i.e. are red)
    current_path_points = np.unique(np.argwhere(cv2.inRange(map, path_color, path_color)), axis=0)
    # Swap columns to get (x, y) format
    current_path_points[:, [1, 0]] = current_path_points[:, [0, 1]]
    # Convert to list of tuples
    current_path_points = list(tuple(point) for point in current_path_points)
    path_points_covered = len(path_covered) - len(current_path_points)
    # Update path to keep points that are not covered by the dynamic obstacles,
    # while preserving the order of the points from the original path
    path_covered = [point for point in path_covered if point in current_path_points]

    if verbose:
      print(f"Path points covered by dynamic obstacle {obstacle_number}: {path_points_covered}")
  
  # Redraw start/goal points to prevent them from being hidden by obstacle
  drawInitialPoints(map, start, goal)
  drawPathPoints(map, path_covered, path_color, verbose)

  if verbose:
    print(f"Total path points covered by new dynamic obstacles: {original_path_length - len(path)}")

  print(f"{num_dynamic_obstacles} dynamic obstacles generated successfully!")
