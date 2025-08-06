import subprocess

import gcsim as gcsim_module


def gcsim(*args):
    return subprocess.run([gcsim_module.gcsim_binary_path()] + list(args))
