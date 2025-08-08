import argparse
import os
import sys

from .util import gcsim


def main():
    parser = argparse.ArgumentParser(
        description="Run gcsim optimizer.",
        usage="gcsim-optimizer filename [additional_arguments]",
    )
    parser.add_argument("filename", help="The name of the config file to process.")
    parser.add_argument(
        "additional_arguments",
        nargs="*",
        help="Additional arguments to pass to gcsim.",
    )
    args = parser.parse_args()

    config_file_path = args.filename
    argument = " ".join(args.additional_arguments)

    base_filename = os.path.basename(config_file_path)
    output_filename, _ = os.path.splitext(base_filename)
    output_filename += ".json"

    viewer_json_dir = "viewer_json"
    os.makedirs(viewer_json_dir, exist_ok=True)

    output_file_path = os.path.join(viewer_json_dir, output_filename)

    if not os.path.exists(config_file_path):
        print(f"Error: Input file not found at {config_file_path}")
        sys.exit(1)

    try:
        print(f"Running substat optimization for {config_file_path}...")
        # First gcsim command
        gcsim("-c", config_file_path, "-s", "-substatOptimFull")

        print(f"Generating viewer file for {config_file_path}...")
        # Second gcsim command
        # We need to handle the case where 'argument' is an empty string.
        command = ["-c", config_file_path, "-out", output_file_path, "-gz=false"]
        if argument:
            command.append(argument)
        
        gcsim(*command)

        print("Script finished successfully.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
