#!/usr/bin/env python3
import glob
import re
import argparse
import os
import json

# can't find a google version
CELL_URL = 'https://antmicro-skywater-pdk-docs.readthedocs.io/en/test-submodules-in-rtd/contents/libraries/sky130_fd_sc_ls/cells/'


# Print the summaries
def summarize(cell_count):
    script_dir = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(script_dir, 'categories.json')) as fh:
        categories = json.load(fh)
    with open(os.path.join(script_dir, 'defs.json')) as fh:
        defs = json.load(fh)

    # print all used cells, sorted by frequency
    total = 0
    if args.print_summary:
        print('# Cell usage')
        print()
        print('| Cell Name | Description | Count |')
        print('|-----------|-------------|-------|')
        for name, count in sorted(cell_count.items(), key=lambda item: item[1], reverse=True):
            category = categories['map'][name]
            if count > 0:
                total += count
                cell_link = f'{CELL_URL}{name}'
                print(f'| [{name}]({cell_link}) | {defs[name]["description"]} |{count} |')

        print(f'| | Total | {total} |')

    if args.print_category:
        by_category = {}
        for cell_name in cell_count:
            cat_index = categories['map'][cell_name]
            cat_name = categories['categories'][cat_index]
            if cat_name in by_category:
                by_category[cat_name]['count'] += cell_count[cell_name]
                by_category[cat_name]['examples'].append(cell_name)
            else:
                by_category[cat_name] = { 'count' : cell_count[cell_name], 'examples' : [cell_name] }

        print('# Cell usage by Category')
        print()
        print('| Category | Cells | Count |')
        print('|---------------|----------|-------|')
        for cat_name, cat_dict in sorted(by_category.items(), key=lambda x: x[1]['count'], reverse=True):
            cell_links = [ f'[{name}]({CELL_URL}{name})' for name in cat_dict['examples'] ]
            print(f'|{cat_name} | {" ".join(cell_links)} | {cat_dict["count"]}|')


# Parse the lib, cell and drive strength an OpenLane gate-level Verilog file
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
    return (cell_count)


# Load all the json defs and combine into one big dict, keyed by cellname
def create_defs(args):
    # replace this with a find
    json_files = glob.glob('sky130_fd_sc_hd/latest/cells/*/definition.json')
    definitions = {}
    for json_file in json_files:
        with open(json_file) as fh:
            definition = json.load(fh)
            definitions[definition['name']] = definition

    with open('defs.json', 'w') as fh:
        json.dump(definitions, fh)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tiny Tapeout summary tool")

    parser.add_argument('--create-defs', help="create def file", action="store_const", const=True, default=False)
    parser.add_argument('--print-summary', help="print summary", action="store_const", const=True, default=False)
    parser.add_argument('--print-category', help="print category", action="store_const", const=True, default=False)
    parser.add_argument('--gl', help="gate level netlist")
    args = parser.parse_args()

    # create map
    if args.create_defs:
        create_defs(args)
    elif args.gl:
        cell_count = get_cell_count_from_gl(args)
        summarize(cell_count)
    else:
        parser.print_help()
