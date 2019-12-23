# Copyright (c) 2019 Hiroki Takemura (kekeho)
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from docopt import docopt
from lib import split

DOC = """
_  _  ___   ____ 
( \/ )(__ \ ( ___)
 \  /  / _/  )__) 
  \/  (____)(__)  

v2f: Video -> Frames
Copyright: Hiroki Takemura (kekeho) 2019 All Rights Reserved.
This software is released under the MIT License.
https://github.com/kekeho/v2f

Usage:
    v2f <video_filename> [-i <interval_count>] [-f <fps>]


Options:
    -i,--interval <interval_count>    Generate frame image per interval
    -f, --fps <fps>                   Give fps info
    -h, --help                        Show this help
"""


def main():
    args = docopt(DOC)

    filename = str(args['<video_filename>'])
    interval = int(args['--interval']) if args['--interval'] else 1
    fps_info = float(args['--fps']) if args['--fps'] else None

    split.split(filename, interval, fps_info)


if __name__ == '__main__':
    main()
