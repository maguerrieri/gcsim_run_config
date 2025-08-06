#!/usr/bin/env python3

import argparse
import re
from pathlib import Path

from .util import gcsim


WEAPONS_PATH = Path('weapons')


def generate_script(script_filename: Path, weapon_input: str, character_input: str):
    if not script_filename.exists():
        print(f"Script file {script_filename} does not exist.")
        return
    with open(script_filename, 'r') as f:
        script = f.read()

    weapon_path = (WEAPONS_PATH / weapon_input).with_suffix('.txt')
    if not weapon_path.exists():
        print(f"{weapon_input}.txt not found in current directory")
        return
    with open(weapon_path, 'r') as f:
        weapons = f.read().splitlines()

    if character_input not in script.split():
        print(f"{character_input} not found in script")
        return

    out_path = Path(f'{character_input} {weapon_input} output')
    out_path.mkdir(parents=True, exist_ok=True)
    for weapon in weapons:
        lines = script.split('\n')
        for i, line in enumerate(lines):
            if line.startswith(f'{character_input} add weapon'):
                lines[i] = re.sub(r'weapon=".+?"', f'weapon="{weapon}"', line)
        new_script = '\n'.join(lines)
        file_path = (out_path / weapon).with_suffix('.txt')
        with open(file_path, 'w') as f:
            f.write(new_script)

    print(f"Generated scripts for {character_input} with {weapon_input} weapons in {out_path}.")


def main():
    parser = argparse.ArgumentParser(description="Generate weapon scripts for a character.")
    parser.add_argument("script_file", help="The script file to process")
    weapons = Path('weapons').glob('*.txt')
    parser.add_argument("weapon_type", help=f"The type of weapon to use", choices=[w.stem for w in weapons])
    parser.add_argument("character_name", help="The name of the character; must be present in the script file")
    args = parser.parse_args()

    generate_script(Path(args.script_file), args.weapon_type, args.character_name)
