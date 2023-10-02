#!/usr/bin/env python3

import argparse
import pathlib
import subprocess


parser = argparse.ArgumentParser(description="open json file given rule or chapter abbreviation e.g. kd1, bu-pc35")
parser.add_argument("abbr")
parser.add_argument("-c", help="Open comment file")
parser.add_argument("-r", help="Open root file")
args = parser.parse_args()

abbr = args.abbr
if abbr.startswith("bi") or abbr.startswith("bu"):
    book = abbr[0:2]
    rule_class = abbr[3:5]
    number = abbr[5:]
elif abbr.startswith("kd"):
    book = abbr[0:2]
    number = abbr[2:]
elif abbr.startswith("pvr"):
    book = abbr[0:3]
    number = abbr[3:]

json_filename = "/Users/tracy/Development/bilara-data/translation/en/brahmali/vinaya"
bilara_type = "translation"
if args.c:
    json_filename = "/Users/tracy/Development/bilara-data/comment/en/brahmali/vinaya"
    bilara_type = "comment"
elif args.r:
    json_filename = "/Users/tracy/Development/bilara-data/root/pli/ms/vinaya"
    bilara_type = "root"

if bilara_type == "root":
    print("still todo")
else:
    if book in ["bi", "bu"]:
        json_filename += f"/pli-tv-{book}-vb/pli-tv-{book}-vb-{rule_class}/pli-tv-{book}-vb-{rule_class}{number}_{bilara_type}-en-brahmali.json"
    else:
        json_filename += f"/pli-tv-{book}/pli-tv-{abbr}_{bilara_type}-en-brahmali.json"

# Check whether file exists before opening.
if pathlib.Path(json_filename).is_file():
    subprocess.run(["vi", json_filename])
else:
    print(f"File does not exist: {json_filename}")
