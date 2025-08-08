from pathlib import Path

from gcsim_run_config.config import PlainTextConfigType, Test, load_config


def test_load_yaml_config():
    config = load_config(Path("tests/same_character.yaml"))
    assert config[0] == Test(
        character="bennett",
        test=Test.ArtifactTest(
            weapon_name="archaicpetra",
            artifact_sets=[["no", "esf"], ["esf"]]
            )
        )
    assert config[1] == Test(
        character="bennett",
        test=Test.ArtifactTest(
            weapon_name="blizzardstrayer",
            artifact_sets=[["esf", "no"], ["no"]]
            )
        )
    assert config[2] == Test(
        character="bennett",
        test=Test.WeaponTest(
            artifact_set=["no"],
            weapons=["bloodstainedchivalry"]
            )
        )
    assert config[3] == Test(
        character="bennett",
        test=Test.ArtifactTest(
            weapon_name="bloodstainedchivalry",
            artifact_sets=[["no"], ["esf"]]
            )
        )

def test_load_plain_text_config():
    config = load_config(Path("tests/plain_weapons"), config_type=PlainTextConfigType.WEAPON, character="some_character")
    assert config == [Test(
        character="some_character",
        test=Test.WeaponTest(
            artifact_set=None,
            weapons=["a", "b", "c"]
        )
    )]

