import glob
import os

def deleteImages(verbose: bool = False) -> None:
  """
  Delete all PNG files in the image folders.
  """
  
  if verbose:
    print("Deleting old images...")

  # Get list of files in the image folders
  files = glob.glob('./ai_robotics_final_project/map/images/*/*.png')

  # Delete all files in the images folder
  for f in files:
    os.remove(f)

  if verbose:
    print("Old images deleted successfully!")
