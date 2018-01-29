"""Command line interface for the live-preview program.
Usage:
  preview-markup [options] [<text_file>]

Arguments:
  <text_file>    Markdown/ReST file or search directory [default: .]

Options:
  -v, --verbose  make more noise
  -q, --quiet    make less noise

Last Change: 2018-01-29
URL: https://github.com/xolox/python-preview-markup
"""

# Standard library modules.
import logging
import os
import sys

# External dependencies.
from argopt import argopt
import coloredlogs

# Modules included in our package.
from preview_markup.converter import find_readme_file
from preview_markup.server import start_webserver
from preview_markup import __version__


def main():
    """Command line interface for the ``preview`` program."""
    # Initialize logging to the terminal.
    logger = logging.getLogger(__name__)
    coloredlogs.install()
    # Parse the command line arguments.
    args = argopt(__doc__, version=__version__).parse_args()
    if args.verbose:
        coloredlogs.increase_verbosity()
    elif args.quiet:
        coloredlogs.decrease_verbosity()
    try:
        if os.path.isdir(args.text_file):
            start_webserver(find_readme_file(args.text_file))
        elif os.path.isfile(args.text_file):
            start_webserver(args.text_file)
        else:
            raise IOError("Input doesn't exist!")
    except KeyboardInterrupt:
        sys.stderr.write('\r')
        logger.error("Interrupted by Control-C, terminating ..")
        sys.exit(1)
    except Exception:
        logger.exception("Encountered an unhandled exception, terminating!")
        sys.exit(1)
