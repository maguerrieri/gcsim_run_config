import logging
import shutil
from pathlib import Path

import pytest

from gcsim_batcher.generate import (Mode, _output_directory_name,
                                    generate_artifacts_scripts,
                                    generate_multi_scripts)


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, force=True)


@pytest.fixture
def artifact_test_env(tmp_path, monkeypatch):
    """A fixture to set up the test environment in a temporary directory."""
    # Copy real test files to the temporary directory
    test_src_dir = Path(__file__).parent
    shutil.copy(test_src_dir / "ChevSaraBen.txt", tmp_path)
    shutil.copy(test_src_dir / "plain_artifacts", tmp_path)
    
    monkeypatch.chdir(tmp_path)
    
    script_file = Path("ChevSaraBen.txt")
    artifacts_file = Path("plain_artifacts")
    
    yield script_file, artifacts_file, tmp_path


def test_generate_artifact_scripts(artifact_test_env):
    script_file, artifacts_file, tmp_path = artifact_test_env
    
    output_directory = tmp_path / "generated_scripts"
    
    artifact_sets = [s.split() for s in artifacts_file.read_text().strip().splitlines()]
    generate_artifacts_scripts(
        script_file,
        "bennett",
        None,
        artifact_sets,
        output_directory
    )

    assert output_directory.is_dir()

    expected_files = {
        "bennett_artifacts_no_esf.txt",
        "bennett_artifacts_no.txt",
        "bennett_artifacts_esf.txt",
    }
    generated_files = {f.name for f in output_directory.iterdir()}
    assert generated_files == expected_files

    # Check file contents
    for sets in artifact_sets:
        file_name = f"bennett_artifacts_{'_'.join(sets)}.txt"
        file_path = output_directory / file_name
        assert file_path.is_file()
        
        content = file_path.read_text()
        count = 2 if len(sets) > 1 else 4
        for s in sets:
            assert f'bennett add set="{s}" count={count};' in content
        
        # Check that the old set is not present
        assert 'bennett add set="crimsonwitch" count=4;' not in content


@pytest.fixture
def multi_test_env(tmp_path, monkeypatch):
    """A fixture to set up the test environment for multi mode in a temporary directory."""
    test_src_dir = Path(__file__).parent
    shutil.copy(test_src_dir / "ChevSaraBen.txt", tmp_path)
    shutil.copy(test_src_dir / "same_character.yaml", tmp_path)
    
    monkeypatch.chdir(tmp_path)
    
    script_file = Path("ChevSaraBen.txt")
    config_file = Path("same_character.yaml")
    
    yield script_file, config_file, tmp_path


def test_generate_multi_scripts_default_output(multi_test_env):
    script_file, config_file, tmp_path = multi_test_env

    generate_multi_scripts(
        script_file,
        config_file,
        _output_directory_name(None, script_file, "bennett", Mode.MULTI)
    )

    default_output_dir = tmp_path / "configs"
    assert default_output_dir.is_dir()

    assert len(list(default_output_dir.iterdir())) > 0
    logger.debug(list(default_output_dir.iterdir()))
    for directory in default_output_dir.iterdir():
        assert not directory.is_file()
        for file in directory.iterdir():
            assert file.is_file()


def test_generate_multi_scripts_specified_output(multi_test_env):
    script_file, config_file, tmp_path = multi_test_env
    
    output_directory = tmp_path / "custom_root"
    
    from gcsim_batcher.generate import generate_multi_scripts
    generate_multi_scripts(
        script_file,
        config_file,
        output_directory
    )

    assert output_directory.is_dir()
    assert not (tmp_path / "configs").exists()
    assert len(list(output_directory.iterdir())) > 0
    for directory in output_directory.iterdir():
        assert not directory.is_file()
        for file in directory.iterdir():
            assert file.is_file()
