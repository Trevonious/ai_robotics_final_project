def getFormattedMapTitle(filename_suffix: str, number: int) -> str:
  """
  Get the formatted map title.

  @param filename_suffix: The filename suffix
  @param number: The number of the map
  @return: The formatted title of the map
  """

  title = "Map " + str(number)

  if filename_suffix != "":
    # Replace underscores with spaces
    suffix = filename_suffix.replace("_", " ")
    # Capitalize the first letter of each word
    title += " - " + suffix.title()
  
  return title
