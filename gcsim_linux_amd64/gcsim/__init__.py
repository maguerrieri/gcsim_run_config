from pathlib import Path


def gcsim_binary_path():
    return Path(__file__).parent / "bin" / "gcsim_linux_amd64"
