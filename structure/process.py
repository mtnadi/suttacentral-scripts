#!/usr/bin/env python3

from collections import OrderedDict
import json
import os


def new_filename(filename, data_type):
    assert filename[-5:] == ".json", f"{filename} is not a .json file"
    assert data_type in ("name", "tree")
    return filename[:-5] + "-" + data_type + ".json"

def name_filename(filename, debug=False):
    if debug:
        return "./name-sandbox.json"
    return new_filename(filename, "name")

def tree_filename(filename, debug=False):
    if debug:
        return "./tree-sandbox.json"
    return new_filename(filename, "tree")

def split_file(filename, super_names, debug=False):
    # Read in .json file.
    with open(filename) as f:
        data = json.load(f)

    # These will hold the final structures we need.
    tree = None
    names = None

    # The first element is handled differently than the rest.
    first = True
    for entry in data:
        # Assert that there are no keys that have not been mentioned in the ticket.
        for key in entry.keys():
            assert key in ["_path", "name", "num", "child_count", "display_num", "type", "acronym", "volpage", "biblio_uid", "grandparent"], f"Unknown key found: {key}"

        # To create the tree, we need to split up the path into bits, and then make
        # a tree.
        split_path = entry["_path"].split("/")

        if first:
            # Initialize tree and names.
            tree = {split_path[-1]: []}
            names = {split_path[-1]: OrderedDict()}
            super_names[split_path[-1]] = entry["name"]
            first = False
        else:
            # Fill in tree.
            parent = tree[split_path[0]]
            for i in range(1, len(split_path) - 1):
                keys = [list(d.keys())[0] for d in parent]
                parent = parent[keys.index(split_path[i])][split_path[i]]
            if "type" in entry and entry["type"] != "text":
                parent.append({split_path[-1]: []})
            else:
                parent.append(split_path[-1])

            # Fill in names.
            names[split_path[0]][split_path[-1]] = entry["name"]

    if debug:
        import pprint
        pprint.pprint(names)
#        pprint.pprint(tree)

    with open(name_filename(filename, debug), 'w') as json_file:
        json.dump(names, json_file, indent = 2, ensure_ascii=False)
    with open(tree_filename(filename, debug), 'w') as json_file:
        json.dump(tree, json_file, indent = 2, ensure_ascii=False)


# Loop over all .json files.
directory = "/Users/tracy/Development/sc-data/structure/division"
# HACK def:
one_file = "/Users/tracy/Development/sc-data/structure/division/sutta/dn.json"
one_file = "/Users/tracy/Development/sc-data/structure/division/vinaya/pli-tv-bu-pm.json"
super_names = {}  # TODO read in from .json and run sanity check
for root, dirs, files in os.walk(directory):
    for file in files:
        filename = os.path.join(root, file)
        # Select just one file HACK
        if filename != one_file:
            continue
        # END HACK
        print(f"Processing {filename}")
        split_file(filename, super_names, debug=True)

import pprint; pprint.pprint(super_names)
