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

def split_file(filename, division_set, super_name, debug=False):
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
            # Initialize tree and names.  Collect info for super-tree/name.
            tree = {split_path[-1]: []}
            names = {split_path[-1]: OrderedDict()}
            assert split_path[-1] not in division_set, f"Duplicate division path name {split_path[-1]}"
            division_set.add(split_path[-1])
            assert super_name[split_path[-1]] == "", f"Name already filled for {split_path[-1]}"
            super_name[split_path[-1]] = entry["name"]
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
        pprint.pprint(tree)

    with open(name_filename(filename, debug), "w") as json_file:
        json.dump(names, json_file, indent=2, ensure_ascii=False)
    with open(tree_filename(filename, debug), "w") as json_file:
        json.dump(tree, json_file, indent=2, ensure_ascii=False)


# Loop over all .json files.
directory = "/Users/tracy/Development/sc-data/structure/division"

# Read in super-name.json to fill it out.
with open("super-name.json") as f:
    super_name = OrderedDict(json.load(f))

# Collect all the divisions we'll process into a set.
division_set = set()

# HACK def:
one_file = "/Users/tracy/Development/sc-data/structure/division/sutta/dn.json"
one_file = "/Users/tracy/Development/sc-data/structure/division/vinaya/pli-tv-bu-pm.json"
for root, dirs, files in os.walk(directory):
    for file in files:
        filename = os.path.join(root, file)
        # Select just one file HACK
        if filename != one_file:
            continue
        # END HACK
        print(f"Processing {filename}")
        split_file(filename, division_set, super_name, debug=True)

# Sanity!  Check that all leaves of super-tree exactly match the divisions we've collected.
division_set_source = set()
with open("super-tree.json") as f:
    super_tree = json.load(f)

def find_leaves(obj, division_set_source):
    if type(obj) == list:
        for x in obj:
            find_leaves(x, division_set_source)
    elif type(obj) == dict:
        for k,v in obj.items():
            assert type(v) == list
            find_leaves(v, division_set_source)
    else:
        division_set_source.add(obj)
find_leaves(super_tree[0], division_set_source)
assert division_set_source == division_set, "Leaves in super_tree.json don't match divisions we collected"

# Sanity!  Check we've filled out everything in super-name.
for k, v in super_name.items():
    if v == "":
        print(f"No name for key {k}")
# Write out super-name.json into a new file.
with open("sandbox-super-name.json", "w") as json_file:
    json.dump(super_name, json_file, indent=2, ensure_ascii=False)

