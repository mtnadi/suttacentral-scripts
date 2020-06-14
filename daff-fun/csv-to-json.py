#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Convert a csv'd json bilara-data file back into json.  The csv if edited in OpenOffice should be saved with Character set UTF-8, Field delimiter {Tab}, and Quote all text cells unchecked")
parser.add_argument("filename", help="The csv file to convert")
parser.add_argument("--dest", action="store", dest="dest", help="Specify destination filename")
parser.add_argument("-v", action="store_true", help="Print each line of new file")
args = parser.parse_args()

csv_filename = args.filename
if csv_filename[-4:] != ".csv":
    raise ValueError("Invalid file")

json_filename = args.dest if args.dest else csv_filename[:-3] + "new.json"
print(f"creating {json_filename}...")

with open(json_filename, "w") as f:
    f.write("{\n")
    with open(csv_filename) as c:
        for line in c:
            [x, y] = line.strip("\n").split("\t")
            out_line = f'  "{x}": "{y}",\n'
            if args.v:
                print(out_line)
            f.write(out_line)
    f.write("}")
    print("TODO: remove trailing comma from last line")
