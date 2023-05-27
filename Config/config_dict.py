"""Convert workbook data into a dictionary that can be passed to other modules for later use."""

import csv
import logging
import pandas as pd

# Create logger
logger = logging.getLogger(__name__)


def config_data(json_data):
  """Read config workbook based on file type and create a dictionary."""
  # Declare variables and constants
  CONFIG_PATH = json_data.pop("config_path")
  
  # Declare empty dictionary for return
  data = {}
  
  # If filepath provided, see if file exists. If file doesn't exist, return empty dictionary.
  ff not CONFIG_PATH.is_file():
    logger.warning("File path provided is not a file")
    return data
  
  # If file extension is csv
  if CONFIG_PATH.suffix == ".csv":
    # Read csv config
    with open(CONFIG_PATH, "r") as f:
      temp = csv.DictReader(f)
      for line in temp:
        data[line["Setting"]] = line["value"]
  
  # If file extension is xlsx
  if CONFIG_PATH.suffix == ".xlsx":
    
    # Create a constants dictionary
    constants_df = pd.read_excel(CONFIG_PATH, "Constants", header=0)
    constants_name = constants_df["Constant Name"]
    constants_value = constants_df["Constant Value"]
    constants_dict = dict(zip(constants_name, constants_value))
    
    # Set settings sheet name based on environment
    settings_sheet = f'{constants_dict.pop("Environment")} Settings'
    
    # Read settings based on environment from constants dictionary
    settings_df = pd.read_excel(CONFIG_PATH, settings_sheet, header=0)
    
    # Filter data to look for names
    settings_name = settings_df["Setting Name"]
    
    # Filter data to look for values
    settings_value = settings_df["Setting Value"]
    
    # Convert series to dictionary and return
    settings_dict = dict(zip(settings_name, settings_value))
  
  # Combine settings, constants and json into one dictionary
  data = {**settings_dict, **constants_dict, **json_data}
  
  return data

if __name__ == "__main__":
  from config_json import json_data
  from logger_module import logger
  data = config_data(json_data)
  logger.debug(f"dictionary data: {data}")
