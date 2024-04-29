'''Executes the app'''

import sys
import argparse
from RNMNApp import RNMNApp

def main(arguments):
    parser = argparse.ArgumentParser()

    parser.add_argument("-ng","--no_gui", help="Deactivates the graphic user interface",
                         action=argparse.BooleanOptionalAction, default=False)

    args = parser.parse_args(arguments)

    main_app = RNMNApp(gui=args.no_gui)

    main_app.start_app()


if __name__=='__main__':
    main(sys.argv[1:])
