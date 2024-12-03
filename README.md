# Prerequisites

- Install Python 3.13.0
- Ensure the necessary modules are installed (cv2, numpy, etc.)

# Instructions

In cmd or terminal window, navigate to the directory above the project (_cd .._)
and run the following command:

- _py -m ai_robotics_final_project_

The flags available are:

- _-ms \<number\>_ or --map_size \<number\>: The length and width of the map, in pixels (default=400; min=100; max=1000)

- _-ndo \<number\>_ or _--num_dynamic_obstacles \<number\>_: The number of initial obstacles to generate (default=2; min=1; max=0.5% of map_size)

- _-nio \<number\>_ or _--num_initial_obstacles \<number\>_: The number of initial obstacles to generate (default=20; min=1; max=5% of map_size)

- _-nm \<number\>_ or _--num_maps \<number\>_: The number of maps to generate (default=1)

- _-rmi \<number\>_ or _--rrt_max_iterations \<number\>_: The maximum iterations for the RRT algorithm (default=4000; min=1,000; max=8,000)

- _-rss \<number\>_ or _--rrt_step_size \<number\>_: The step size for the RRT algorithm (default=4; min=1; max=1% of map_size)

- _-rt \<number\>_ or _--replanning_threshold \<number\>_: The replanning encountered obstacle threshold for the D* algorithm (default=4; min=1; max=0.5%% of map_size)

- _-v \<True/False\>_ or _--verbose \<True/False\>_: Whether or not to print more detailed output in the console (default=False)

Below are examples of running with flags:

- _py -m ai_robotics_final_project -v True_

- _py -m ai_robotics_final_project -nio 15_

- _py -m ai_robotics_final_project -ms 800 -ndo 4 -nio 40 -rmi 5000 -rss 8 -rt 4 -v True_

When you close a map image, the program will continue execution.
