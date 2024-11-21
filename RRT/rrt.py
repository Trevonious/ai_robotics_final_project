import cv2
import numpy as np
import random
import time

# Select random start and goal in free space
def selectPoints(map, verbose: bool = False) -> tuple:
    """
    Selects random start and goal points in the free (white) spaces of the map.

    @param map: The map image with obstacles
    @param verbose: Whether or not to print verbose output (default is False)
    @return: The start and goal points in the map
    """
    print("Randomly selecting start and goal points...")
    
    free_spaces = np.argwhere(map == 255)
    free_spaces = [(pt[1], pt[0]) for pt in free_spaces]
    
    start, goal = random.sample(free_spaces, 2)
    # Start point in green
    cv2.circle(map, start, 10, (0, 255, 0), -1)
    # Goal point in blue
    cv2.circle(map, goal, 10, (255, 0, 0), -1)
    
    print("Start and goal points selected!")

    if verbose:
        print(f"Start point (green): {start}")
        print(f"Goal point (blue): {goal}")

    return start, goal

# Check if the line between two points intersects obstacles
def isCollisionFree(map, point1, point2):
    line = np.linspace(point1, point2, num=100, dtype=int)
    for x, y in line:
        if map[y, x] == 0:  # Black pixel indicates obstacle
            return False
    return True

def RRT(map, start, goal, max_iterations=1000, step_size=10, verbose=False):
    """
    Implements the Rapidly-Exploring Random Tree (RRT) algorithm.

    @param map: The map image with obstacles
    @param start: The start position
    @param goal: The goal position
    @param max_iterations: Maximum number of iterations for the RRT
    @param step_size: The step size for tree expansion
    @param verbose: Whether or not to print verbose output
    @return: The path found by the RRT algorithm
    """
    rows, cols = map.shape
    nodes = [start]
    parent = {start: None}
    start_time = time.time()

    for _ in range(max_iterations):
        # Random point in map
        rand_point = (random.randint(0, cols - 1), random.randint(0, rows - 1))
        # Find nearest node
        nearest_node = min(nodes, key=lambda node: np.linalg.norm(np.array(node) - np.array(rand_point)))

        # Steer towards the random point
        direction = np.array(rand_point) - np.array(nearest_node)
        length = np.linalg.norm(direction)
        if length == 0:
            continue
        direction = direction / length
        new_point = tuple((np.array(nearest_node) + step_size * direction).astype(int))

        # Check collision
        if 0 <= new_point[0] < cols and 0 <= new_point[1] < rows and isCollisionFree(map, nearest_node, new_point):
            nodes.append(new_point)
            parent[new_point] = nearest_node
            # Draw on map for visualization
            cv2.line(map, nearest_node, new_point, (0, 255, 255), 1)

            # Check if goal is reached
            if np.linalg.norm(np.array(new_point) - np.array(goal)) < step_size:
                parent[goal] = new_point
                end_time = time.time()
                print("Goal reached in", end_time - start_time, "seconds!")
                break

    # Reconstruct path
    path = []
    if goal in parent:
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
    else:
        print("Failed to find a path.")

    if verbose:
        print("Path length:", len(path))

    return path

