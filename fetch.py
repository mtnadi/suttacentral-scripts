#!/usr/bin/env python3

import argparse
import pathlib
import subprocess

BILARA_DATA_DIR = "/home/nadi/Development/bilara-data"


parser = argparse.ArgumentParser(description="open json file given rule or chapter abbreviation e.g. kd1, bu-pc35")
parser.add_argument("abbr")
parser.add_argument("-c", action="store_true", help="Open comment file")
parser.add_argument("-r", action="store_true", help="Open root file")
args = parser.parse_args()

abbr = args.abbr
sutta = False
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
elif abbr.startswith("an") or abbr.startswith("sn"):
    collection = abbr[0:2]
    dot = abbr.find(".")
    book = abbr[2:dot]
    number = abbr[dot + 1:]
    sutta = True
elif abbr.startswith("mn") or abbr.startswith("dn"):
    collection = abbr[0:2]
    number = abbr[2:]
    sutta = True
elif abbr.startswith("thag") or abbr.startswith("thig") or abbr.startswith("cp"):
    if abbr.startswith("cp"):
        collection = f"kn/{abbr[0:2]}"
    else:
        collection = f"kn/{abbr[0:4]}"
    sutta = True
else:
    print(f"Can't handle {abbr} yet")

if sutta:
    json_filename = f"{BILARA_DATA_DIR}/translation/en/sujato/sutta"
    bilara_type = "translation"
    language = "en-sujato"
    if args.c:
        json_filename = f"{BILARA_DATA_DIR}/comment/en/sujato/sutta"
        bilara_type = "comment"
    elif args.r:
        json_filename = f"{BILARA_DATA_DIR}/root/pli/ms/sutta"
        bilara_type = "root"
        language = "pli-ms"

    if collection in ["an", "sn"]:
        json_filename += f"/{collection}/{collection}{book}/{abbr}_{bilara_type}-{language}.json"
    else:
        json_filename += f"/{collection}/{abbr}_{bilara_type}-{language}.json"

else:
    json_filename = f"{BILARA_DATA_DIR}/translation/en/brahmali/vinaya"
    bilara_type = "translation"
    language = "en-brahmali"
    if args.c:
        json_filename = f"{BILARA_DATA_DIR}/comment/en/brahmali/vinaya"
        bilara_type = "comment"
    elif args.r:
        json_filename = f"{BILARA_DATA_DIR}/root/pli/ms/vinaya"
        bilara_type = "root"
        language = "pli-ms"

    if book in ["bi", "bu"]:
        if rule_class == "as":
            print("still TODO")
        else:
            json_filename += f"/pli-tv-{book}-vb/pli-tv-{book}-vb-{rule_class}/pli-tv-{book}-vb-{rule_class}{number}_{bilara_type}-{language}.json"
    else:
        json_filename += f"/pli-tv-{book}/pli-tv-{abbr}_{bilara_type}-{language}.json"

# Check whether file exists before opening.
if pathlib.Path(json_filename).is_file():
    subprocess.run(["vi", json_filename])
else:
    print(f"File does not exist: {json_filename}")
