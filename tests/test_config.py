from pathlib import Path

from gcsim_batcher.config import PlainTextConfigType, Test, load_config


def test_load_yaml_config():
    root_path, config = load_config(Path("tests/same_character.yaml"))
    assert root_path is None
    assert config[0] == Test(character="bennett",
                             test=Test.ArtifactTest(weapon_name="absolution",
                                                    artifact_sets=[["no", "esf"], ["esf"]]))
    assert config[1] == Test(character="bennett",
                             test=Test.ArtifactTest(weapon_name="amenomakaguechi",
                                                    artifact_sets=[["esf", "no"], ["no"]]))
    assert config[2] == Test(character="bennett",
                             test=Test.WeaponTest(artifact_set=["no"],
                                                  weapons=["aquilafavonia"]))
    assert config[3] == Test(character="bennett",
                             test=Test.ArtifactTest(weapon_name="aquilafavonia",
                                                    artifact_sets=[["no"], ["esf"]],
                                                    output_directory="custom_output"))

def test_load_plain_weapons_config():
    root_path, config = load_config(Path("tests/plain_weapons"),
                                    config_type=PlainTextConfigType.WEAPON,
                                    character="some_character")
    assert root_path is None
    assert config == [
        Test(character="some_character",
             test=Test.WeaponTest(artifact_set=None,
                                  weapons=["a", "b", "c"])
        )
    ]


def test_load_plain_artifacts_config():
    root_path, config = load_config(Path("tests/plain_artifacts"),
                                    config_type=PlainTextConfigType.ARTIFACT,
                                    character="some_character")
    assert root_path is None
    assert config == [
        Test(character="some_character",
             test=Test.ArtifactTest(weapon_name=None,
                                    artifact_sets=[["no", "esf"], ["no"], ["esf"]])
        )
    ]
