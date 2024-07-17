from . import cli
from .logging import log

if __name__ == "__main__":
    try:
        cli()
    except Exception as error:
        log.warn(error)
        exit(1)
