
import logging
from logging.handlers import RotatingFileHandler
import enum


def create_rotating_log(path):
    """
    Creates a rotating log
    """
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=1024*100,
                                  backupCount=5)
    logger.addHandler(handler)

    return logger



# Enum for size units
class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4


def convert_unit(size_in_bytes, unit):
   """ Convert the size from bytes to other units like KB, MB or GB"""
   if unit == SIZE_UNIT.KB:
       return size_in_bytes/1024
   elif unit == SIZE_UNIT.MB:
       return size_in_bytes/(1024*1024)
   elif unit == SIZE_UNIT.GB:
       return size_in_bytes/(1024*1024*1024)
   else:
       return size_in_bytes


def print_speed(label, speed_in_bytes_per_sec):
    """Print a speed in MB/s"""
    print("{!s} is {!s} MB/s".format(label, convert_unit(speed_in_bytes_per_sec, SIZE_UNIT.MB)))

