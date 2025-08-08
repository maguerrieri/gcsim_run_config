#!/usr/bin/env python3

import argparse
import logging
import re
from pathlib import Path
from typing import NamedTuple

from .util import DEBUG


logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)


def read_script(script_path: Path, character_name: str):
    if not script_path.exists():
        logger.error(f"Script file {script_path} does not exist.")
        return None

    with open(script_path, 'r') as f:
        script = f.read()

    if character_name not in script:
        logger.error(f"{character_name} not found in script")
        return None

    return script


def update_weapon(script_lines: list[str], character_name: str, weapon_name: str, refine: int):
    new_lines = []
    for i, line in enumerate(script_lines):
        if line.startswith(f'{character_name} add weapon'):
            new_lines.append(f"{character_name} add weapon=\"{weapon_name}\" refine={refine} lvl=90/90;")
        else:
            new_lines.append(line)
    return new_lines


def generate_weapon_scripts(script_path: Path, character_name: str, artifact_sets: list[str] | None, weapons: list[str]):
    script = read_script(script_path, character_name)
    if script is None:
        return

    out_path = Path(f'{character_name}_weapons')
    out_path.mkdir(parents=True, exist_ok=True)

    script_lines = script.splitlines()
    if artifact_sets:
        script_lines = update_artifact_sets(script_lines, character_name, artifact_sets)

    def make_file_name(weapon: str, refine: int):
        if artifact_sets:
            return f"{character_name}_{'_'.join(artifact_sets)}_weapon_{weapon}_r{refine}.txt"
        else:
            return f"{character_name}_weapon_{weapon}_r{refine}.txt"

    for weapon, refine in [(weapon, refine) for refine in (1, 5) for weapon in weapons]:
        lines = update_weapon(script_lines, character_name, weapon, refine)
        new_script = '\n'.join(lines)
        file_path = (out_path / make_file_name(weapon, refine)).with_suffix('.txt')
        with open(file_path, 'w') as f:
            f.write(new_script)

    logger.info(f"Generated scripts for {character_name} with weapons: {weapons}.")
    logger.info(f"Scripts saved in {out_path}.")


def update_artifact_sets(script_lines: list[str], character_name: str, artifact_sets: list[str]):
    replaced = False
    new_lines = []
    count = 2 if len(artifact_sets) == 2 else 4
    for i, line in enumerate(script_lines):
        if line.startswith(f'{character_name} add set'):
            if not replaced:
                # Replace the first occurrence of the artifact set
                for set_ in artifact_sets:
                    new_lines.append(f"{character_name} add set=\"{set_}\" count={count};")
                replaced = True
            else:
                # Remove subsequent occurrences
                pass
        else:
            new_lines.append(line)
    if not replaced:
        logger.error(f"No artifact sets found for {character_name} in the script.")
    return new_lines


Weapon = NamedTuple('Weapon', [('name', str), ('refine', int)])


def generate_artifacts_scripts(script_path: Path,
                               character_name: str,
                               weapon: Weapon | None,
                               artifact_sets: list[list[str]]):
    script = read_script(script_path, character_name)
    if script is None:
        return

    out_path = Path(f'{character_name}_artifacts')
    out_path.mkdir(parents=True, exist_ok=True)

    script_lines = script.splitlines()
    if weapon:
        script_lines = update_weapon(script_lines, character_name, weapon.name, weapon.refine)

    def make_file_name(set: list[str]):
        if weapon:
            return f"{character_name}_{weapon.name}_{weapon.refine}_artifacts_{'_'.join(set)}.txt"
        else:
            return f"{character_name}_artifacts_{'_'.join(set)}.txt"

    for sets in artifact_sets:
        existing_sets = re.findall(rf"{character_name} add set=(?P<set>.*) count=[0-9];", script)
        if not existing_sets:
            logger.error(f"No artifact sets found for {character_name} in the script.")
            return

        if len(existing_sets) > 1:
            logger.debug(f"Multiple sets found for {character_name}: {existing_sets}.")
            logger.info(f"Multiple sets found for {character_name}; replacing the first and removing the others.")

        updated_lines = update_artifact_sets(script_lines, character_name, sets)
        if updated_lines is None:
            return

        new_script = '\n'.join(updated_lines)
        file_name = make_file_name(sets)
        file_path = out_path / file_name
        with open(file_path, 'w') as f:
            f.write(new_script)

        logger.info(f"Generated scripts for {character_name} with 2pc artifact combinations in {out_path}.")


def generate_multi_scripts(script_file: Path, test_configuration_file: Path):
    if not test_configuration_file.exists():
        logger.error(f"Test configuration file {test_configuration_file} does not exist.")
        return

    from gcsim_batcher.config import (  # Import here to avoid circular imports
        Test, load_config)
    config = load_config(test_configuration_file)

    for test in config:
        if isinstance(test.test, Test.ArtifactTest):
            for refine in (1, 5):
                logger.info(f"Generating artifact scripts for character {test.character} with weapon {test.test.weapon_name}, refine {refine}, sets {test.test.artifact_sets}.")
                if test.test.weapon_name:
                    weapon = Weapon(test.test.weapon_name, refine)
                else:
                    weapon = None
                generate_artifacts_scripts(script_file, test.character, weapon, test.test.artifact_sets)
        elif isinstance(test.test, Test.WeaponTest):
            logger.info(f"Generating weapon scripts for character {test.character} with artifact set {test.test.artifact_set}, weapons {test.test.weapons}.")
            generate_weapon_scripts(script_file, test.character, test.test.artifact_set, test.test.weapons)
        else:
            logger.warning(f"Unknown test type for character {test.character}. Skipping.")


def main():
    parser = argparse.ArgumentParser(description="Generate testing scripts for a character.")
    parser.add_argument("script_file", help="The script file to process", type=Path)

    subparsers = parser.add_subparsers(required=True)

    weapon_parser = subparsers.add_parser("weapon", help="Generate weapon scripts")
    weapon_parser.add_argument("character_name", help="The name of the character; must be present in the script file")
    weapon_parser.add_argument("file", help="The weapon input file", type=Path)
    weapon_parser.set_defaults(func=lambda args: generate_weapon_scripts(args.script_file, args.character_name, None, args.file.read_text().strip().splitlines()))

    artifact_parser = subparsers.add_parser("artifact", help="Generate artifact scripts")
    artifact_parser.add_argument("character_name", help="The name of the character; must be present in the script file")
    artifact_parser.add_argument("file", help="The artifact input file", type=Path)
    artifact_parser.set_defaults(func=lambda args: generate_artifacts_scripts(args.script_file, args.character_name, None, args.file.read_text().strip().splitlines()))

    multi_parser = subparsers.add_parser("multi", help="Generate scripts from various combinations of character, weapon, and artifact sets")
    multi_parser.add_argument("test_configuration_file", help="Configuration file for the test", type=Path)
    multi_parser.set_defaults(func=lambda args: generate_multi_scripts(args.script_file, args.test_configuration_file))

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
