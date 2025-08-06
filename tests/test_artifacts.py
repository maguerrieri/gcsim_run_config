from pathlib import Path
from gcsim_run_config.artifacts import generate_artifacts_scripts


def test_generate_artifacts_scripts():
    # Arrange
    script_file = Path('tests/ChevSaraBen.txt')
    set_type = '4pc'
    character_name = 'bennett'
    artifact_sets = ['ap', 'instructor']

    # Act
    generate_artifacts_scripts(script_file, set_type, character_name, artifact_sets)

    # Assert
    output_dir = Path(f'{character_name} artifacts {set_type} output')
    assert output_dir.exists()
    assert len(list(output_dir.glob('*.txt'))) == len(artifact_sets)
