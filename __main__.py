import cv2
from ai_robotics_final_project.d_star.d_star import *
from ai_robotics_final_project.map.generate_maps import generateMaps

# Main execution
solutions_folder_path = './ai_robotics_final_project/map/images/solutions/'
map_number = 1
maps = generateMaps()

for map in maps:
  start, goal = selectPoints(map)
  path = dStar(map, start, goal)

  # Visualize
  for point in path:
    map[(point[0], point[1])] = (0, 0, 255)  # Path in red

  cv2.imshow('Path', map)
  cv2.waitKey(0)
  cv2.imwrite(solutions_folder_path + "map" + str(map_number) + "_solution.png", map)
  cv2.destroyAllWindows()
  map_number += 1
