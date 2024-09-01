#!/usr/bin/env python3

import argparse
import pathlib
import subprocess

BILARA_DATA_DIR = "/home/nadi/Development/sc/bilara-data"

# TODO pts vp refs e.g.
# S. IV, 142
# Vin. I, 22
# A. III, 187
# Perhaps open file directly or spit out the range it covers (for short suttas)


parser = argparse.ArgumentParser(description="open json file given rule or chapter abbreviation e.g. kd1, bu-pc35")
parser.add_argument("abbr")
parser.add_argument("-c", action="store_true", help="Open comment file")
parser.add_argument("-m", action="store_true", help="Open html file")
parser.add_argument("-r", action="store_true", help="Open root file")
parser.add_argument("-d", action="store_true", help="Run git diff with published")
parser.add_argument("-e", action="store_true", help="Run git diff --color-words=. with published")
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
elif abbr.startswith("an") or (abbr.startswith("sn") and not abbr.startswith("snp")):
    collection = abbr[0:2]
    dot = abbr.find(".")
    book = abbr[2:dot]
    number = abbr[dot + 1:]
    sutta = True
elif (abbr.startswith("mn") and not abbr.startswith("mnd")) or abbr.startswith("dn"):
    collection = abbr[0:2]
    number = abbr[2:]
    sutta = True
elif abbr.startswith("thag") or abbr.startswith("thig"):
    collection = f"kn/{abbr[0:4]}"
    sutta = True
elif abbr.startswith("cp") or abbr.startswith("kp"):
    collection = f"kn/{abbr[0:2]}"
    sutta = True
elif abbr.startswith("snp") or abbr.startswith("ud"):
    dot = abbr.find(".")
    if abbr.startswith("ud"):
        book = abbr[0:2]
        vagga = abbr[2:dot]
    else:
        book = abbr[0:3]
        vagga = abbr[3:dot]
    number = abbr[dot + 1:]
    collection = f"kn/{book}/vagga{vagga}"
    sutta = True
elif abbr.startswith("iti"):
    itivaggas = {
            1: [1, 10],
            2: [11, 20],
            3: [21, 27],
            4: [28, 37],
            5: [38, 49],
            6: [50, 59],
            7: [60, 69],
            8: [70, 79],
            9: [80, 89],
            10: [90, 99],
            11: [100, 112]}
    def get_iti_vagga(number):
        for vagga, [start, finish] in itivaggas.items():
            if number > finish:
                next
            elif number >= start:
                return vagga
        else:
            print(f"Something funny with {abbr}.  iti runs from 1 to 112")
    number = int(abbr[3:])
    vagga = get_iti_vagga(number)
    collection = f"kn/iti/vagga{vagga}"
    sutta = True
else:
    print(f"Can't handle {abbr} yet")
    exit()

if sutta:
    json_filename = f"{BILARA_DATA_DIR}/translation/en/sujato/sutta"
    bilara_type = "translation"
    language = "-en-sujato"
    if args.c:
        json_filename = f"{BILARA_DATA_DIR}/comment/en/sujato/sutta"
        bilara_type = "comment"
    elif args.m:
        json_filename = f"{BILARA_DATA_DIR}/html/pli/ms/sutta"
        bilara_type = "html"
        language = ""
    elif args.r:
        json_filename = f"{BILARA_DATA_DIR}/root/pli/ms/sutta"
        bilara_type = "root"
        language = "-pli-ms"

    if collection in ["an", "sn"]:
        json_filename += f"/{collection}/{collection}{book}/{abbr}_{bilara_type}{language}.json"
    else:
        json_filename += f"/{collection}/{abbr}_{bilara_type}{language}.json"

else:
    json_filename = f"{BILARA_DATA_DIR}/translation/en/brahmali/vinaya"
    bilara_type = "translation"
    language = "-en-brahmali"
    if args.c:
        json_filename = f"{BILARA_DATA_DIR}/comment/en/brahmali/vinaya"
        bilara_type = "comment"
    elif args.m:
        json_filename = f"{BILARA_DATA_DIR}/html/pli/ms/vinaya"
        bilara_type = "html"
        language = ""
    elif args.r:
        json_filename = f"{BILARA_DATA_DIR}/root/pli/ms/vinaya"
        bilara_type = "root"
        language = "-pli-ms"

    if book in ["bi", "bu"]:
        if rule_class == "as":
            print("still TODO")
        else:
            json_filename += f"/pli-tv-{book}-vb/pli-tv-{book}-vb-{rule_class}/pli-tv-{book}-vb-{rule_class}{number}_{bilara_type}{language}.json"
    else:
        json_filename += f"/pli-tv-{book}/pli-tv-{abbr}_{bilara_type}{language}.json"

# Check whether file exists before opening.
if pathlib.Path(json_filename).is_file():
    if args.d:
        # Run git diff against branch published.
        # Note: current directory must be within bilara-data.
        subprocess.run(["git", "diff", "published", "--", json_filename])
    elif args.e:
        # Run git diff --color-words=. against branch published.
        # Note: current directory must be within bilara-data.
        subprocess.run(["git", "diff",  "--color-words=.", "published", "--", json_filename])
    else:
        # Open the file.
        subprocess.run(["vi", json_filename])
else:
    print(f"File does not exist: {json_filename}")
