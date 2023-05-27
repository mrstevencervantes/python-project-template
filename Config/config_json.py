"""Convert JSON file into a dictionary that can be passed to other modules for later use."""
import json
import logging
from pathlib import Path

# Create logger
logger = logging.getLogger(__name__)


def config_json(filepath):
    """Read JSON file and create a dictionary."""
    # Get working dir
    temp = []
    for part in Path.cwd().parts:
        if part.lower() != "automation":
            temp.append(part)
        elif part.lower() == "automation":
            temp.append(part)
            break
    WORKING_DIR = Path("/".join(temp))

    # Declare empty dictionary for return
    json_data = {}

    # If filepath provided, see if file exists. If file doesn't exist, raise exception
    path = Path.joinpath(WORKING_DIR,filepath)
    path.is_file()
    if not path.is_file():
        raise Exception("Config JSON does not exist.")

    # Read JSON file and convert data into a dictionary
    with open(path) as f:
        json_data = json.load(f)

    # Create file paths for later use
    json_data["config_path"] = Path.joinpath(WORKING_DIR,json_data.pop("config_path"))
    json_data["logger_path"] = Path.joinpath(WORKING_DIR,json_data.pop("logger_path"))
    json_data["work_dir"] = WORKING_DIR
    json_data["parent_dir"] = WORKING_DIR.parent

    return json_data


if __name__ == "__main__":
    from logger_module import logger
    json_data = config_json('Config/Config.json')
    logger.debug(f'JSON dictionary data: {json_data}')
else:
    json_data = config_json('Config/Config.json')
