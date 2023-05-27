"""Main file to run {Name} script. Please see README.md and config file for more info."""

import os
import csv
import traceback
from pathlib import Path
from datetime import datetime

from Config.config_json import json_data
from Config.logger_module import logger
from Config.config_dict import config_data

# Create data dictionary
DATA = config_data(json_data)


def main(data):
    """Main function to be run."""
    logger.debug(f"Starting main function.")
    successful_run = False

    try:
        main_function()
    except Exception as e:
        successful_run = False
        logger.exception(
            f"A fatal error has occured during this run. {str(e)} Please review the debugger log and the Error Stack Trace text file.")
        log_exception(Path.joinpath(PARENT_DIRECTORY, data.get("ErrorOutput")))
    else:
        successful_run = True
        logger.debug("No errors during automation run.")
    finally:
        try:
            with open(Path.joinpath(PARENT_DIRECTORY, data.get("LogFile")), newline='', mode='a') as log_file:
                log_file_writer = csv.writer(
                    log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                log_file_writer.writerow(
                    [SCRIPT_NAME, datetime.now(), os.environ['USERNAME'], str(successful_run)])
        except Exception as e:
            logger.exception(
                f"A fatal error has occured while attempting to log details of this run. {str(e)} Unable to write log.")

    logger.debug(f"Main function completed.")


def log_exception(filename):
    """Write out exceptions."""
    logger.debug("Writing error to file.")
    try:
        with open(filename, "w") as f:
            f.write(f"{datetime.now()}\n")
            f.write(traceback.format_exc())
    except FileNotFoundError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred. {str(e)} Please review logs. Unable to continue.")
    else:
        logger.debug("Error writing completed.")


if __name__ == "__main__":
    script_name = DATA.get("parent_dir").name
    logger.info(f"Starting automation {script_name}...")
    main(DATA)
    logger.info("Automation completed.")
