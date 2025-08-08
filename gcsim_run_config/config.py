import logging
import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import yaml
import yamlcore

from .util import DEBUG


logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO, force=DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class Test:
    """
    Represents a test configuration for a character, which can be either an ArtifactTest or WeaponTest.
    """

    @dataclass
    class ArtifactTest:
        weapon_name: str | None
        artifact_sets: list[list[str]]
        def __post_init__(self):
            logger.debug(f"Creating ArtifactTest with weapon_name={self.weapon_name} and artifact_sets={self.artifact_sets}")
            for artifact_set in self.artifact_sets:
                if len(artifact_set) < 1 or len(artifact_set) > 2:
                    raise ValueError(f"Invalid artifact set: {artifact_set}. Must be a single set or a pair of sets.")

    @dataclass
    class WeaponTest:
        artifact_set: list[str] | None
        weapons: list[str]

    type Test = ArtifactTest | WeaponTest

    character: str
    test: Test


class PlainTextConfigType(StrEnum):
    WEAPON = "weapon"
    ARTIFACT = "artifact"


def _config_from_yaml_list(data: list, character: str | None = None) -> list[Test]:
    """
    Convert a YAML dictionary to a list of Test objects.
    """
    def _parse_test(item: dict) -> Test:
        def _parse_test(item: dict) -> Test.Test:
            """
            Parse a test configuration from a dictionary.
            """
            if 'artifact_sets' in item:
                return Test.ArtifactTest(item['weapon'], item['artifact_sets'])
            elif 'weapons' in item:
                return Test.WeaponTest(item['artifact_set'], item['weapons'])
            else:
                raise ValueError(f"Invalid test configuration in YAML data: {item}.")

        return Test(character=item.get('character', character), test=_parse_test(item))

    return [_parse_test(item) for item in data]


def load_config(file: Path, config_type: PlainTextConfigType | None = None, character: str | None = None) -> list[Test]:
    """
    Load a configuration file; this may either be YAML, in which case it contains a list of configuration objects (see
    schema for details), or a plain test file containing a list of weapon or artifact names. In the latter case, which
    type of test is loaded depends on the `config_type` parameter.
    """
    if not file.exists():
        raise FileNotFoundError(f"Configuration file {file} does not exist.")
    if file.suffix == '.yaml':
        with open(file, 'r') as f:
            data = yaml.load(f, Loader=yamlcore.CoreLoader) # `yamlcore` doesn't parse `no` as `False` 🙄
            logger.debug(f"Loaded YAML data from {file}: {data} (type {type(data)})")
            if isinstance(data, list):
                return _config_from_yaml_list(data)
            elif isinstance(data, dict):
                if 'character' in data and 'tests' in data:
                    logger.debug(f"loading {file} as YAML with character {data['character']} and tests {data['tests']}")
                    return _config_from_yaml_list(data['tests'], character=data['character'])
                else:
                    raise ValueError("YAML file must contain a character and list of configuration objects.")
            else:
                raise ValueError("YAML file must contain a list of configuration objects.")

    if config_type is None or character is None:
        raise ValueError("config_type and character must be specified for plain text files.")

    with open(file, 'r') as f:
        content = f.read().strip().splitlines()

    if config_type == PlainTextConfigType.WEAPON:
        return [Test(character=character, test=Test.WeaponTest(artifact_set=None, weapons=content))]
    elif config_type == PlainTextConfigType.ARTIFACT:
        return [Test(character=character, test=Test.ArtifactTest(weapon_name=None, artifact_sets=[line.split(" ") for line in content]))]
    else:
        raise ValueError(f"Unsupported config type: {config_type}")
