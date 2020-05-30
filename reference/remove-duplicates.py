import argparse

parser = argparse.ArgumentParser(description="remove duplicate instances of references")
parser.add_argument("filename", help="The json file to process")
parser.add_argument("--dest", help="Specify destination filename")
parser.add_argument("-v", action="store_true", help="Verbose mode")
args = parser.parse_args()

json_filename = args.filename
if json_filename[-5:] != ".json":
    raise ValueError("Invalid file")

new_filename = json_filename + ".new"
print(f"creating {new_filename} . . .")


def remove_duplicates(astring):
    """
    Returns a new string exactly the same as astring except duplicate entries are removed

    Assumes that astring is of one of the formats:
        "ref, ref, ref",
        "ref, ref, ref"
    """
    # get at text without leading and trailing " and ,
    contents = astring.strip('",')
    # split into individual references
    refs = contents.split(", ")
    # make it a set!
    cleaned_refs = set(refs)
    # sort it
    cleaned_refs = sorted(cleaned_refs)
    # rebuild the full string
    ret = '"' + ", ".join(cleaned_refs) + '"'
    if astring[-1] == ",":
        ret += ","
    return ret


with open(new_filename, "w") as newfile:
    with open(json_filename) as srcfile:
        for line in srcfile:
            if line.strip() not in ["{", "}"]:
                [x, y] = line.strip().split(": ", 1)
                new_y = remove_duplicates(y)
                cleaned_line = f'  {x}: {new_y}\n'
                newfile.write(cleaned_line)
                if args.v:
                    print(line)
                    print(cleaned_line)
            else:
                newfile.write(line)
