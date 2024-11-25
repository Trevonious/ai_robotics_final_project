import cv2
import math
import numpy as np
import random

def drawInitialPoints(map: list, start: tuple, goal: tuple) -> None:
  """
  Draws the start and goal points on the map.

  @param map: The map image with obstacles
  @param start: The start point
  @param goal: The goal point
  """

  # Draw start point in green
  cv2.circle(map, (start[0], start[1]), 10, (0, 255, 0), -1)
  # Draw goal point in blue
  cv2.circle(map, (goal[0], goal[1]), 10, (255, 0, 0), -1)

def drawPathPoints(map: list, path: list, color: tuple, verbose: bool = False) -> None:
  """
  Draws the points for the provided path.

  @param map: The map image with obstacles
  @param path: The path to draw
  @param color: The color to draw the path (default is red)
  @param verbose: Whether or not to print verbose output (default is False)
  """

  if verbose:
    print("Drawing solution path...")

  for point in path:
    # Draw path in red
    map[(point[1], point[0])] = color

def heuristic(a: tuple, b: tuple) -> int:
  """
  Finds the Manhattan distance between two points.

  @param a: The first point
  @param b: The second point
  @return: The Manhattan distance between the two points
  """

  return abs(a[0] - b[0]) + abs(a[1] - b[1])

def clearPaths(
  map: list,
  start: cv2.typing.Point,
  goal: cv2.typing.Point,
  verbose: bool = False
) -> None:
  """
  Clears paths from the provided map.

  @param map: The map image with obstacles
  @param start: The start point
  @param goal: The goal point
  @param verbose: Whether or not to print verbose output (default is False)
  """

  if verbose:
    print("Clearing paths from map...")

  # Clear path by setting all red pixels to white
  map[np.all(map == [0, 0, 255], axis=-1)] = [255, 255, 255]
  # Clear path by setting all orange pixels to white
  map[np.all(map == [0, 155, 255], axis=-1)] = [255, 255, 255]
  # Redraw start and goal points
  drawInitialPoints(map, start, goal)

  if verbose:
    print("Paths cleared from map successfully!")

def selectInitialPoints(map: list, verbose: bool = False) -> tuple:
  """
  Selects random start and goal points in the free (white) spaces of the map.

  @param map: The map image with obstacles
  @param verbose: Whether or not to print verbose output (default is False)
  @return: The start and goal points in the map
  """

  if verbose:
    print("Randomly selecting start and goal points...")

  # Find all white spaces
  free_spaces = np.unique(np.argwhere(map == 255)[:,0:2], axis=0)
  # Remove duplicate arrays
  free_spaces = np.unique(free_spaces, axis=0)
  # Swap columns to get (x, y) format
  free_spaces[:, [1, 0]] = free_spaces[:, [0, 1]]
  start, goal = random.sample(list(free_spaces), 2)

  if verbose:
    print("Start point (green): (" + str(start[0]) + ", " + str(start[1]) + ")")
    print("Goal point (blue): (" + str(goal[0]) + ", " + str(goal[1]) + ")")
  
  drawInitialPoints(map, start, goal)
  
  print("Start and goal points selected successfully!")
  print()

  return (start[0], start[1]), (goal[0], goal[1])

def selectPathPoint(path: list, verbose: bool = False) -> tuple:
  """
  Selects a random point along the path.

  @param path: The path to select a point from
  @param verbose: Whether or not to print verbose output (default is False)
  @return: The selected point
  """

  if verbose:
    print("Selecting random point along path...")

  minimum_distance_from_initial_points = math.floor(len(path) * 0.15)
  # Select a random point along the path, within the acceptable index range
  path_point = random.choice(
    path[
      minimum_distance_from_initial_points
      :
      len(path) - minimum_distance_from_initial_points + 1
    ]
  )

  if verbose:
    print("Random point selected: (" + str(path_point[0]) + ", " + str(path_point[1]) + ")")

  return (path_point[0], path_point[1])
