#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


ARTIFACTS_PATH = Path('artifacts')


def generate_artifacts_scripts(script_filename: Path, set_type: str, character_name: str, artifact_sets: list[str] | None = None):
    if not script_filename.exists():
        print(f"Script file {script_filename} does not exist.")
        return
    with open(script_filename, 'r') as f:
        script = f.read()

    artifacts_path = (ARTIFACTS_PATH / 'artifacts').with_suffix('.txt')
    if not artifacts_path.exists():
        print(f"{artifacts_path} not found in artifacts directory")
        return
    with open(artifacts_path, 'r') as f:
        sets = f.read().splitlines()

    if artifact_sets:
        sets = [s for s in sets if s.split()[0] in artifact_sets]

    if character_name not in script.split():
        print(f"{character_name} not found in script")
        return

    if set_type == '4pc':
        out_path = Path(f'{character_name} artifacts 4pc output')
        out_path.mkdir(parents=True, exist_ok=True)
        for set_line in sets:
            set_parts = set_line.split()
            set_name = set_parts[0]
            set_count = set_parts[1] if len(set_parts) > 1 else 4
            new_lines = []
            sets_found = 0
            for line in script.split('\n'):
                if line.startswith(f'{character_name} add set'):
                    sets_found += 1
                    if sets_found == 1:
                        new_line = re.sub(r'set=".+?"', f'set="{set_name}"', line)
                        if set_count is not None:
                            new_line = re.sub(r'count=\d+', f'count={set_count}', new_line)
                        new_lines.append(new_line)
                else:
                    new_lines.append(line)
            new_script = '\n'.join(new_lines)
            with open(out_path / f'{set_name}.txt', 'w') as f:
                f.write(new_script)
        print(f"Generated scripts for {character_name} with 4pc artifacts in {out_path}.")
    elif set_type == '2pc':
        out_path = Path(f'{character_name} artifacts 2pc output')
        out_path.mkdir(parents=True, exist_ok=True)

        for i in range(len(sets)):
            for j in range(i + 1, len(sets)):
                set1 = sets[i].split()[0]
                set2 = sets[j].split()[0]
                lines = script.split('\n')
                new_lines = []
                insertion_index = None

                for index, line in enumerate(lines):
                    if line.startswith(f'{character_name} add set'):
                        if insertion_index is None:
                            insertion_index = index
                    else:
                        new_lines.append(line)

                if insertion_index is not None:
                    new_lines.insert(insertion_index, f'{character_name} add set="{set2}" count=2;')
                    new_lines.insert(insertion_index, f'{character_name} add set="{set1}" count=2;')

                new_script = '\n'.join(new_lines)

                output_filename = out_path / f'{set1}_{set2}.txt'
                with open(output_filename, 'w') as f:
                    f.write(new_script)
        print(f"Generated scripts for {character_name} with 2pc artifact combinations in {out_path}.")


def main():
    parser = argparse.ArgumentParser(description="Generate artifact scripts for a character.")
    parser.add_argument("script_file", help="The script file to process")
    parser.add_argument("set_type", help="The type of set to use", choices=['4pc', '2pc'])
    parser.add_argument("character_name", help="The name of the character; must be present in the script file")
    parser.add_argument('-a', '--artifact_sets', nargs='*', help="The artifact sets to use", choices=[s.split()[0] for s in (ARTIFACTS_PATH / 'artifacts').with_suffix('.txt').read_text().splitlines()])
    args = parser.parse_args()

    generate_artifacts_scripts(Path(args.script_file), args.set_type, args.character_name, args.artifact_sets)
