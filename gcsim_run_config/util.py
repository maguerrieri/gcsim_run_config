import os
import subprocess

import gcsim as gcsim_module


DEBUG = os.getenv("DEBUG") is not None


def gcsim(*args):
    return subprocess.run([gcsim_module.gcsim_binary_path()] + list(args))
