import argparse
import logging
from pathlib import Path

from .batch import run_batch


def main():
    logging.basicConfig(level=logging.INFO, force=True)

    parser = argparse.ArgumentParser(
        description="Generate and run a batch of gcsim optimizer commands."
    )
    # This assumes that the script is being run from within the package,
    # so we can use __file__ to find the configs directory.
    configs_dir = Path(__file__).parent / "configs"
    if not configs_dir.exists():
        logging.error(f"Error: Configs directory not found at {configs_dir}")
        # A more robust solution might be to use importlib.resources
        # to locate package data.
        return

    configs = [p.stem for p in configs_dir.glob("*.txt")]
    parser.add_argument(
        "config_type",
        help="The type of config list to use.",
        choices=configs,
    )
    parser.add_argument(
        "input_directory", help="The directory containing the .txt config files."
    )
    parser.add_argument("output_file", help="The name of the output CSV file.")
    args = parser.parse_args()

    config_list_path = (configs_dir / args.config_type).with_suffix(".txt")
    input_dir = Path(args.input_directory)

    if not config_list_path.exists():
        logging.error(f"Error: Config list file not found at {config_list_path}")
        return

    if not input_dir.is_dir():
        logging.error(f"Error: Input directory not found at {input_dir}")
        return

    with open(config_list_path, "r") as f:
        config_names = [line.strip() for line in f if line.strip()]

    commands = []
    for name in config_names:
        file_path = input_dir / f"{name}.txt"
        if file_path.exists():
            commands.append(["gcsim-optimizer", str(file_path)])
        else:
            logging.warning(f"Warning: Config file not found, skipping: {file_path}")

    if not commands:
        logging.error(f"No valid config files found to process.")
        return

    logging.info(f"Running batch with {len(commands)} commands.")

    run_batch(commands, args.output_file)

    logging.info(f"Batch run for '{args.config_type}' complete. Output in '{args.output_file}.csv'")


if __name__ == "__main__":
    main()
