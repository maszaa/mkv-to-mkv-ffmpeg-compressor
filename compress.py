import os
import subprocess
import sys

import configuration

def allowed_path(path, is_file=False):
  is_allowed = is_file is False or any(extension in path for extension in configuration.ALLOWED_VIDEO_FILE_EXTENSIONS)
  is_excluded = any(exclusion in path for exclusion in configuration.EXCLUDED_PATH_PATTERNS)
  is_included_or_not_excluded = (is_excluded is True and
                                 any(inclusion in path for inclusion in configuration.INCLUDED_PATH_PATTERNS) or
                                 is_excluded is False)

  if is_allowed is False:
    configuration.LOGGER.info(f"Path {path} is not allowed\n  is_file: {is_file}\n  allowed extensions: {configuration.ALLOWED_VIDEO_FILE_EXTENSIONS}")
  if is_included_or_not_excluded is False:
    configuration.LOGGER.info(f"Path {path} is not included or is excluded\n  inclusions: {configuration.INCLUDED_PATH_PATTERNS}\n  exclusions: {configuration.EXCLUDED_PATH_PATTERNS}")

  return is_allowed is True and is_included_or_not_excluded is True

def not_compressed(filepath):
  return os.path.isfile(filepath) is False

def create_compressed_files_destination_path(path):
  os.makedirs(path, exist_ok=True)
  configuration.LOGGER.info(f"Created compressed files destination path {path} or it existed already")

def compress_file(source_file, destination_file):
  configuration.LOGGER.info(f"Compressing file {source_file} to file {destination_file}")

  result = subprocess.run(
    [
      *configuration.FFMPEG_INPUT_FILE_PREFIX,
      source_file,
      *configuration.FFMPEG_CONVERSION_PARAMETERS_LIST,
      destination_file
    ],
    capture_output=True
  )

  configuration.LOGGER.info(result.args)

  stdout = result.stdout.decode(sys.stdout.encoding)
  stderr = result.stderr.decode(sys.stderr.encoding)

  if stdout:
    configuration.LOGGER.info(stdout)
  if stderr:
    configuration.LOGGER.error(stderr)

  if result.returncode == 0:
    configuration.LOGGER.info(f"Successfully compressed file {source_file} to file {destination_file}")
  else:
    configuration.LOGGER.error(f"Error occured in compressing file {source_file} to file {destination_file}, check stderr")

  return result.returncode

def handle_path(path, path_relative_to_original_path, files_to_compress):
  path_content = os.listdir(path)

  for path_item in path_content:
    full_path = os.path.join(path, path_item)

    if os.path.isfile(full_path):
      if allowed_path(full_path, is_file=True):
        compressed_destination_filename = os.path.join(configuration.COMPRESSED_FILES_DESTINATION_PATH_PREFIX,
                                                       path_relative_to_original_path,
                                                       path_item)

        if not_compressed(compressed_destination_filename) is True:
          create_compressed_files_destination_path(os.path.join(configuration.COMPRESSED_FILES_DESTINATION_PATH_PREFIX,
                                                                path_relative_to_original_path))

          configuration.LOGGER.info(f"File {full_path} will be compressed")
          files_to_compress[full_path] = compressed_destination_filename
        else:
          configuration.LOGGER.info(f"File {full_path} already compressed")
    else:
      if allowed_path(full_path) is True:
        handle_path(full_path, os.path.join(path_relative_to_original_path, path_item), files_to_compress)

def handle_files_to_be_compressed(files_to_compress):
  for source, destination in sorted(files_to_compress):
    compress_file(source, destination)
