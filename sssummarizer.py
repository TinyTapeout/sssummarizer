#!/usr/bin/env python3
import glob
import re
import argparse
import logging
import os
import sys
import json


def create_map(args):
    # replace this with a find
    json_files = glob.glob('sky130_fd_sc_hd/latest/cells/*/definition.json')
    definitions = []
    for json_file in json_files:
        log.debug(json_file)
        with open(json_file) as fh:
            definitions.append(json.load(fh))

    with open(args.map_file, 'w') as fh:
        json.dump(definitions, fh)


def get_tags():
    with open('tags.json') as fh:
        tags = json.load(fh)
        return tags


def get_cell_count_from_gl(args):
    cell_count = {}
    with open(args.gl) as fh:
        for line in fh.readlines():
            m = re.search('sky130_(\S+)__(\S+)', line)
            if m is not None:
                cell_lib = m.group(1)
                cell_name = m.group(2)
                assert cell_lib in ['fd_sc_hd', 'ef_sc_hd']
                try:
                    cell_count[cell_name] += 1
                except KeyError:
                    cell_count[cell_name] = 0
    return(cell_count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Efabless project tool")

    parser.add_argument('--create-map', help="create map file", action="store_const", const=True)
    parser.add_argument('--print-summary', help="print summary", action="store_const", const=True)
    parser.add_argument('--map', help="map file")
    parser.add_argument('--gl', help="gate level netlist")
    parser.add_argument('--debug', help="debug logging", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    args = parser.parse_args()

    # change directory to the script's path
    os.chdir((os.path.dirname(os.path.realpath(__file__))))

    # setup log
    log_format = logging.Formatter('%(message)s')
    # configure the client logging
    log = logging.getLogger('')
    # has to be set to debug as is the root logger
    log.setLevel(args.loglevel)

    # create console handler and set level to info
    ch = logging.StreamHandler(sys.stdout)
    # create formatter for console
    ch.setFormatter(log_format)
    log.addHandler(ch)

    # create map
    if args.create_map:
        create_map(args)
    elif args.gl:
        cell_count = get_cell_count_from_gl(args)
        summarize(cell_count)
    else:
        parser.print_help()
