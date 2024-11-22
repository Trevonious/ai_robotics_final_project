# Prerequisites

  - Install Python 3.13.0
  - Ensure the necessary modules are installed (cv2, numpy, etc.)

# Instructions

In cmd or terminal window, navigate to the directory above the project (cd ..)
and run the following command:

  py -m ai_robotics_final_project

The flags available are:

  -dim <True/False> or --display_initial_maps <True/False>: Whether or not to display the initially generated maps, one by one (default=False)

  -ms <number> or --map_size <number>: The length and width of the map, in pixels (default=400; min=100; max=1000)

  -ndo <number> or --num_dynamic_obstacles <number>: The number of initial obstacles to generate (default=2; min=1; max=0.5% of map_size)

  -nio <number> or --num_initial_obstacles <number>: The number of initial obstacles to generate (default=20; min=1; max=5% of map_size)

  -nm <number> or --num_maps <number>: The number of maps to generate (default=1)

  -v <True/False> or --verbose <True/False>: Whether or not to print more detailed output in the console (default=False)

Below are examples of running with flags:

  py -m ai_robotics_final_project -v True

  py -m ai_robotics_final_project -dim True -nio 15

  py -m ai_robotics_final_project -dim True -ms 400 -ndo 2 -nio 20 -nm 5 -v True
  

When you close a map image, the program will continue execution.
