#!/usr/bin/env python3
import glob
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

    # only print a description that doesn't match any of these categories
    # not any
    tags = {}

    with open('tags.json.backup') as fh:
        first_run = json.load(fh)
    
    tags['categories'] = ['AND', 'OR', 'NAND', 'NOR', 'clock', 'flop', 'multiplexer', 'latch', 'inverter', 'buffer', 'Fill', 'Tap', 'diode', 'combologic', 'misc']
    tags['map'] = {}
    print(len(definitions))
    for cell_count, d in enumerate(definitions):
        print("-" * 20)
        done = False
        print(cell_count)
        for num, cat in enumerate(tags['categories']):
            print(f'{num} {cat}')
        print()
        print(f'{d["name"]} : {d["description"]}')
        first_run_cat = first_run['map'][d['name']]
        print(first_run_cat)
        tags['map'][d['name']] = first_run_cat
        while(done == False):
            try:
                num = int(input())
            except ValueError as e:
                done = True
                break
            print(tags['categories'][num])
            ok = input("correct? y/n")
            if ok == 'y':
                tags['map'][d['name']] = num
                done = True

    with open("tags.json", 'w') as fh:
        json.dump(tags, fh)

    with open(args.map_file, 'w') as fh:
        json.dump(definitions, fh)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Efabless project tool")

    parser.add_argument('--create-map', help="create map file", action="store_const", const=True)
    parser.add_argument('--map-file', help="map file")
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

    else:
        parser.print_help()
