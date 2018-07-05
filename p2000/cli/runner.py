"""
piton2000

Usage:
  piton2000
  piton2000 scrape
  piton2000 docker --setup
  piton2000 docker --start
  piton2000 docker --stop
  piton2000 -h | --help
  piton2000 -v | --version

Options:
  -h --help                         Show this screen.
  -v --version                      Show version.

Examples:
  piton2000 start

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/MalumAtire832/P2000
"""


from docopt import docopt
from inspect import getmembers, isclass
from pprint import pprint

from p2000 import VERSION


def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)
    # pprint(options)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.iteritems():
        if hasattr(commands, k):
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
