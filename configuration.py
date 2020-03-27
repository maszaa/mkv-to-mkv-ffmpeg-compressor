import logging
import sys

ALLOWED_VIDEO_FILE_EXTENSIONS = [".mkv"]

COMPRESSED_FILES_DESTINATION_PATH_PREFIX = ""

EXCLUDED_PATH_PATTERNS = []
INCLUDED_PATH_PATTERNS = []

FFMPEG_EXECUTABLE_PATH = "/usr/bin/ffmpeg"
FFMPEG_INPUT_FILE_PREFIX = [
  FFMPEG_EXECUTABLE_PATH,
  "-i"
]
FFMPEG_CONVERSION_PARAMETERS = {
  "-vf": "scale=-1:720",
  "-preset": "veryfast",
  "-crf": "23",
  "-c:a": "ac3",
  "-c:s": "dvdsub"
}

LOGGER_NAME = "mkv-to-mkv-ffmpeg-compressor"
LOG_FORMAT = "[%(asctime)-15s: %(levelname)s/%(funcName)s] %(message)s"
LOG_FORMATTER = logging.Formatter(LOG_FORMAT)

LOGGER = logging.getLogger(LOGGER_NAME)
LOGGER.setLevel(logging.DEBUG)

STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
STDOUT_HANDLER.setFormatter(LOG_FORMATTER)
LOGGER.addHandler(STDOUT_HANDLER)

STDERR_HANDLER = logging.StreamHandler(sys.stderr)
STDERR_HANDLER.setFormatter(LOG_FORMATTER)
STDERR_HANDLER.setLevel(logging.ERROR)
LOGGER.addHandler(STDERR_HANDLER)

try:
  from local_configuration import *
except ModuleNotFoundError:
  pass

FFMPEG_CONVERSION_PARAMETERS_LIST = []
[FFMPEG_CONVERSION_PARAMETERS_LIST.extend(item) for item in FFMPEG_CONVERSION_PARAMETERS.items()]
