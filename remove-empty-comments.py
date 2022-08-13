#!/usr/bin/env python3

import argparse
import os.path

# NOTE this doesn't handle files that would end up being empty files, nor
# cleaning up the json if the line removed is the last JSON data line.
# Currently the comma from the previous line would have to be removed
# manually in the latter case.  In the former, the file needs to be deleted
# manually.

parser = argparse.ArgumentParser(description="remove empty comments")
parser.add_argument("filename", help="The json file to process")
parser.add_argument("--dest", help="Specify destination filename")
parser.add_argument("-v", action="store_true", help="Verbose mode")
args = parser.parse_args()

json_filename = args.filename
if json_filename[-5:] != ".json" or "comment" not in json_filename:
    raise ValueError("Invalid file")

if args.dest:
    if os.path.isfile(args.dest):
        reply = input(f"Overwrite {args.dest}? (y/n):").lower().strip()
        if reply != "y":
            print("quitting")
            exit()
    new_filename = args.dest
else:
    new_filename = json_filename + ".new"
print(f"creating {new_filename} . . .")


is_comment_removed = False

with open(new_filename, "w") as newfile:
    with open(json_filename) as srcfile:
        for line in srcfile:
            if line.strip() in ["{", "}"]:
                # These are the first and last lines of the file.
                newfile.write(line)
            else:
                # Handle the actual data.
                [segment_id, content] = line.strip().split(": ", 1)
                if content in ['""', '"",']:
                    # We have an empty comment.  Don't write to new file.
                    is_comment_removed = True
                    if args.v:
                        print(f"Removed {segment_id}")
                else:
                    # Put line into new file.
                    newfile.write(line)

if not is_comment_removed:
    print("No empty comments")
    if json_filename != new_filename:
        os.remove(new_filename)
        print(f"Deleted {new_filename}")
