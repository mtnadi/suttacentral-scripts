import argparse

parser = argparse.ArgumentParser(description="Convert a csv'd json bilara-data file back into json")
parser.add_argument("filename", help="The csv file to convert")
parser.add_argument("--dest", help="Specify destination filename")
parser.add_argument("-v", help="Print each line of new file")
args = parser.parse_args()

csv_filename = args.filename
if csv_filename[-4:] != ".csv":
    raise ValueError("Invalid file")

json_filename = csv_filename.split(".")[0] + "-new.json"
print(f"creating {json_filename}...")

with open(json_filename, "w") as f:
    f.write("{\n")
    with open(csv_filename) as c:
        for line in c:
            [x, y] = line.strip().split(",", 1)
            if args.v:
                print("  " + x + ": " + y + "\n")
            f.write("  " + x + ": " + y + "\n")
    f.write("}\n")
