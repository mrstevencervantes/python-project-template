"""Create logger which can be passed to other modules."""
import logging.config
import yaml
from pathlib import Path

try:
    from Config.config_json import json_data
except ImportError:
    from config_json import json_data


# Read in logger config yaml file with safe load
with open(json_data.pop("logger_path"), 'r') as f:
    config_dict = yaml.safe_load(f)  # Loader=yaml.FullLoader)

# Update logger file path to include the working directory
config_dict["handlers"]["file"]["filename"] = Path.joinpath(json_data.get("work_dir"), config_dict["handlers"]["file"]["filename"])

# create logger
logging.config.dictConfig(config_dict)
logger = logging.getLogger("root")
