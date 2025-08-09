import pytest
from pathlib import Path
import shutil

from gcsim_batcher.generate import generate_artifacts_scripts


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
    
    yield script_file, artifacts_file


def test_generate_artifact_scripts_file_names(artifact_test_env):
    script_file, artifacts_file = artifact_test_env
    
    artifact_sets = [s.split() for s in artifacts_file.read_text().strip().splitlines()]
    generate_artifacts_scripts(
        script_file,
        "bennett",
        None,
        artifact_sets
    )

    output_dir = Path("bennett_artifacts")
    assert output_dir.is_dir()

    expected_files = {
        "bennett_artifacts_no_esf.txt",
        "bennett_artifacts_no.txt",
        "bennett_artifacts_esf.txt",
    }
    generated_files = {f.name for f in output_dir.iterdir()}
    assert generated_files == expected_files

    # Check file contents
    for sets in artifact_sets:
        file_name = f"bennett_artifacts_{'_'.join(sets)}.txt"
        file_path = output_dir / file_name
        assert file_path.is_file()
        
        content = file_path.read_text()
        count = 2 if len(sets) > 1 else 4
        for s in sets:
            assert f'bennett add set="{s}" count={count};' in content
        
        # Check that the old set is not present
        assert 'bennett add set="crimsonwitch" count=4;' not in content


