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

def split_file(filename, all_names, debug=False):
    # Read in .json file.
    with open(filename) as f:
        data = json.load(f)

    # These will hold the final structures we need.
    tree = OrderedDict()
    names = OrderedDict()

    # Cheat.  Go over all the nodes and record whether it is the parent of a
    # leaf node.
    previous_entry = None
    for entry in data:
        if "type" in entry and entry["type"] != "text":
            entry["grandparent"] = True
        elif previous_entry:
            if previous_entry["grandparent"]:
                previous_entry["grandparent"] = False
            entry["grandparent"] = False
        previous_entry = entry

    # Each .json file turns into a list of dicts.
    # Go through each element and pick out the _path and name elements and do
    # whatever we need to do with them.
    for entry in data:
        # Assert that there are no keys that have not been mentioned in the ticket.
        for key in entry.keys():
            assert key in ["_path", "name", "num", "child_count", "display_num", "type", "acronym", "volpage", "biblio_uid", "grandparent"], f"Unknown key found: {key}"

        # To create the tree, we need to split up the path into bits, and then make
        # a tree.
        split_path = entry["_path"].split("/")

        # First check uniqueness of last element of the path.
        all_names.setdefault(split_path[-1], []).append(filename)

        # Traverse the tree until we are at the point where we insert this entry.
        parent = tree
        for i in range(len(split_path) - 1):
            parent = parent[split_path[i]]

        print(split_path)  # TODO remove - debugging
        if "type" in entry and entry["type"] != "text":
            # This is a division or subdivision.  Add it as a key with value [] if
            # the next level will be suttas, {} otherwise.
            if not entry["grandparent"]:
                parent[split_path[-1]] = []
            else:
                parent[split_path[-1]] = OrderedDict()
        else:
            # This is a sutta/text i.e. a leaf.  Append it to the array.
            parent.append(split_path[-1])

        # To create the name lookup, we just need the last bit of the path.
        assert split_path[-1] not in names, f"UID {split_path[-1]} appears more than once."
        names[split_path[-1]] = entry["name"]

    if debug:
        import pprint
        pprint.pprint(names)
        pprint.pprint(tree)

    with open(name_filename(filename, debug), 'w') as json_file:
        json.dump(names, json_file, indent = 2, ensure_ascii=False)
    with open(tree_filename(filename, debug), 'w') as json_file:
        json.dump(tree, json_file, indent = 2, ensure_ascii=False)

# Loop over all .json files.
directory = "/Users/tracy/Development/sc-data/structure/division"
ignore = [
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-dg-bi-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-dg-bu-pm-2.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-dg-bu-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-ka-bu-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-mg-bi-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-mg-bu-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-mi-bi-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-mi-bu-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-mu-bi-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-mu-bu-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-sarv-bi-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-sarv-bu-pm-2.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-sarv-bu-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/pli-tv-bi-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/pli-tv-bu-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/san-lo-bu-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/san-mg-bu-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/san-mu-bu-pm-gbm2.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/san-mu-bu-pm-gbm3.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/san-mu-mpt-bu-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/san-sarv-bi-pm-tf3215.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/san-sarv-bi-pm-tf44.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/san-sarv-bu-pm-tf11.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/xct-mu-bu-pm.json",
]
all_names = {} # later this can be set()
for root, dirs, files in os.walk(directory):
    for file in files:
        filename = os.path.join(root, file)
        if filename in ignore:
            print(f"SKIPPING {filename}")
            continue
        print(f"Processing {filename}")
        split_file(filename, all_names, debug=True)

for name, files in all_names.items():
    if len(files) > 1:
        print(f"Name {name} appears more than once.  Found in {files}")
