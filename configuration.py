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
  "-map": "0",
  "-filter:V:0": "scale=-1:720",
  "-c:V:0": "libx264",
  "-preset": "veryfast",
  "-crf": "23",
  "-c:a": "ac3",
  "-c:s": "copy"
}

def FFMPEG_NOT_ALLOWED_STDERR_CONTENT(content):
  return "error" in content.lower()

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

for key, value in FFMPEG_CONVERSION_PARAMETERS.items():
  item = [key, value]

  if isinstance(value, list):
    item = []
    [item.extend([key, v]) for v in value]

  FFMPEG_CONVERSION_PARAMETERS_LIST.extend(item)
