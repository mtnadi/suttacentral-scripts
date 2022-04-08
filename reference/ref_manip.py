#!/usr/local/opt/python@3.8/bin/python3
from collections import OrderedDict
import csv
import json


ref_file = "main_file.json"
ref_file = "/Users/tracy/Development/bilara-data/reference/pli/ms/vinaya/pli-tv-pvr/pli-tv-pvr12_reference.json"
input_file = "insert_file.csv"
input_file = "../daff-fun/ref12.csv"


def segment_sort_key(segment):
    assert segment.startswith("pli-tv-pvr")
    stringed_key = segment[10:].replace(":", ".").split(".")
    return [int(x) for x in stringed_key]

def refs_only(reference_csv):
    csv_segments = []
    pts_vp_en = []
    pts_cs = []
    pm = []
    references = {}
    with open(input_file) as c:
        csv_reader = csv.reader(c, delimiter="\t")
        for row in csv_reader:
            csv_segments.append(row[0])
            if row[2]:
                pts_vp_en.append(row[2])
                references.setdefault(row[0], []).append(row[2])
            if len(row) >= 4 and row[3]:
                pts_cs.append(row[3])
                references.setdefault(row[0], []).append(row[3])
            if len(row) >= 5 and row[4]:
                pm.append(row[4])
                references.setdefault(row[0], []).append(row[4])
    return references

def add_ref_to_segment(existing_refs, new_refs):
    """Given an existing string of references for a segment, add more refs to it
    and return a comma separated string.

    existing_refs: a string of refs separated by ", ", or an empty string if none
    new_refs: a list of strings
    """
    if existing_refs:
        ref_set = set(existing_refs.split(", "))
        ref_set.update(new_refs)
    else:
        ref_set = set(new_refs)
    return ", ".join(sorted(ref_set))


# Grab the references to insert.
insert_refs = refs_only(input_file)

# Read the reference json file.
with open(ref_file) as f:
    #json_data = json.load(f, object_pairs_hook=OrderedDict)
    json_data = json.load(f)

# Insert the references.
for segment, refs in insert_refs.items():
    print(f"adding {segment}: {refs}")
    json_data[segment] = add_ref_to_segment(json_data.get(segment, default=""), refs)

# Make sure segments are in order.
new_json_data = OrderedDict()
for x in sorted(json_data, key=segment_sort_key):
    new_json_data[x] = json_data[x]

# Spit out a new file.
with open("new_main_file.json", "w") as f:
    json.dump(new_json_data, f, indent=2)
