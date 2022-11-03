#!/usr/bin/env python3
import glob
import re
import argparse
import logging
import os
import sys
import json


# load all the json defs and combine into one big file
def create_defs(args):
    # replace this with a find
    json_files = glob.glob('sky130_fd_sc_hd/latest/cells/*/definition.json')
    definitions = {}
    for json_file in json_files:
        log.debug(json_file)
        with open(json_file) as fh:
            definition = json.load(fh)
            definitions[definition['name']] = definition

    with open('defs.json', 'w') as fh:
        json.dump(definitions, fh)


def summarize(cell_count):
    with open('tags.json') as fh:
        tags = json.load(fh)
    with open('defs.json') as fh:
        defs = json.load(fh)

    # print all used cells
    total = 0
    if args.print_summary:
        print('| cell name | description | count |')
        print('|-----------|-------------|-------|')
        for cell_name in cell_count:
            category = tags['map'][cell_name]
            if cell_count[cell_name] > 0:
                total += cell_count[cell_name]
                cell_link = f'https://google/sky/{cell_name}'
                print(f'| [{cell_link}]({cell_link}) | {defs[cell_name]["description"]} |{cell_count[cell_name]} |')

        print(f'|Total | {total} |')

    if args.print_category:
        by_category = {}
        for cell_name in cell_count:
            category = tags['map'][cell_name]
            by_category[category] = cell_count[cell_name]

        print('| cell category | count |')
        print('|---------------|-------|')
        for index, cat_name in enumerate(tags['categories']):
            try:
                print(f'|{cat_name} | {by_category[index]}|')
            except KeyError:
                pass


def get_cell_count_from_gl(args):
    cell_count = {}
    total = 0
    with open(args.gl) as fh:
        for line in fh.readlines():
            m = re.search(r'sky130_(\S+)__(\S+)_(\d+)', line)
            if m is not None:
                total += 1
                cell_lib = m.group(1)
                cell_name = m.group(2)
                cell_drive = m.group(3)
                assert cell_lib in ['fd_sc_hd', 'ef_sc_hd']
                assert int(cell_drive) > 0
                try:
                    cell_count[cell_name] += 1
                except KeyError:
                    cell_count[cell_name] = 1
    logging.debug(f'total cells = {total}')
    return (cell_count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Efabless project tool")

    parser.add_argument('--create-defs', help="create def file", action="store_const", const=True, default=False)
    parser.add_argument('--print-summary', help="print summary", action="store_const", const=True, default=False)
    parser.add_argument('--print-category', help="print category", action="store_const", const=True, default=False)
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
    if args.create_defs:
        create_defs(args)
    elif args.gl:
        cell_count = get_cell_count_from_gl(args)
        summarize(cell_count)
    else:
        parser.print_help()
