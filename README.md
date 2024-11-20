# Prerequisites

  - Install Python 3.13.0
  - Install the necessary modules (cv2, numpy, etc.)

# Instructions

In cmd or terminal window, navigate to the directory above the project and run
the following command:

  py -m ai_robotics_final_project

The flags available are:

  -d <True/False> or --display <True/False>: Display generated maps, one by one (default is False)
  -nm <number> or --num_maps <number>: The number of maps to generate (default is 1)
  -no <number> or --num_obstacles <number>: The number of obstacles to generate (default is 20)
  -tr' <True/False> or --test_run <True/False>: Whether or not this is a test run (default is False)
  -v <True/False> or --verbose <True/False>: Verbose output (default is False)

Below are examples of running with flags:

  py -m ai_robotics_final_project -v True
  py -m ai_robotics_final_project -d True -no 15
  py -m ai_robotics_final_project -d True -nm 5 -no 10 -tr True -v True
