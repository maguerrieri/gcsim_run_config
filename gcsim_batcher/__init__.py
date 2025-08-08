import sys

from .util import gcsim as gcsim_command


def gcsim():
    try:
        gcsim_command(*sys.argv[1:])
    except KeyboardInterrupt:
        pass
