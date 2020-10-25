#!/usr/bin/env python3

from collections import OrderedDict
import json


# Start with hard-coded file to process.
filename = "/Users/tracy/Development/sc-data/structure/division/sutta/sn.json"
name_filename = "./name-sandbox.json"
tree_filename = "./tree-sandbox.json"

# Read in .json file.
with open(filename) as f:
    data = json.load(f)

# These will hold the final structures we need.
tree = OrderedDict()
names = OrderedDict()

# Cheat.  Go over all the nodes and record whether it is the parent of a leaf node.
previous_entry = None
for entry in data:
    if "type" in entry and entry["type"] != "text":
        entry["grandparent"] = True
    else:
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
    # Traverse the tree until we are at the point where we insert this entry.
    parent = tree
    for i in range(len(split_path) - 1):
        parent = parent[split_path[i]]

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

import pprint
pprint.pprint(names)
pprint.pprint(tree)

with open(name_filename, 'w') as json_file:
    json.dump(names, json_file, indent = 2, ensure_ascii=False)
with open(tree_filename, 'w') as json_file:
    json.dump(tree, json_file, indent = 2, ensure_ascii=False)
