import sys

from compress import handle_path, handle_files_to_be_compressed

def main(argv):
  if len(argv) != 1:
    raise ValueError("Invalid amount of arguments passed, please pass one (input file directory)")

  files_to_be_compressed = {}
  handle_path(argv[0], "", files_to_be_compressed)
  handle_files_to_be_compressed(files_to_be_compressed)

if __name__ == "__main__":
  main(sys.argv[1:])
