#!/usr/local/opt/python@3.8/bin/python3
from collections import OrderedDict
import csv
import json


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
    with open(reference_csv) as c:
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

def insert_refs(ref_json, insert_csv, new_json):
    # Grab the references to insert.
    insert_refs = refs_only(insert_csv)

    # Read the reference json file.
    with open(ref_json) as f:
        json_data = json.load(f)

    # Insert the references.
    for segment, refs in insert_refs.items():
        print(f"adding {segment}: {refs}")
        json_data[segment] = add_ref_to_segment(json_data.get(segment, ""), refs)

    # Make sure segments are in order.
    new_json_data = OrderedDict()
    for x in sorted(json_data, key=segment_sort_key):
        new_json_data[x] = json_data[x]

    # Spit out a new file.
    with open(new_json, "w") as f:
        json.dump(new_json_data, f, indent=2)

files = [
    "ref1.1.csv",
    "ref1.2.csv",
    "ref1.3.csv",
    "ref1.4.csv",
    "ref1.5.csv",
    "ref1.6.csv",
    "ref1.7.csv",
    "ref1.8.csv",
    "ref1.9.csv",
    "ref1.10.csv",
    "ref1.11.csv",
    "ref1.12.csv",
    "ref1.13.csv",
    "ref1.14.csv",
    "ref1.15.csv",
    "ref1.16.csv",
    "ref2.1.csv",
    "ref2.2.csv",
    "ref2.3.csv",
    "ref2.4.csv",
    "ref2.5.csv",
    "ref2.6.csv",
    "ref2.7.csv",
    "ref2.8.csv",
    "ref2.9.csv",
    "ref2.10.csv",
    "ref2.11.csv",
    "ref2.12.csv",
    "ref2.13.csv",
    "ref2.14.csv",
    "ref2.15.csv",
    "ref2.16.csv",
    "ref3.csv",
    "ref4.csv",
    "ref5.csv",
    "ref6.csv",
    "ref7.csv",
    "ref8.csv",
    "ref9.csv",
    "ref10.csv",
    "ref11.csv",
    "ref12.csv",
    "ref13.csv",
    "ref14.csv",
    "ref15.csv",
    "ref16.csv",
    "ref17.csv",
    "ref18.csv",
    "ref19.csv",
    "ref20.csv",
    "ref21.csv",
]

for insert_csv in files:
    assert insert_csv[:3] == "ref" and insert_csv[-4:] == ".csv", "Funky filename.  Expected filename ref[blah].csv"

    chapter = insert_csv[3:-4]
    root_ref_json = f"/Users/tracy/Development/bilara-data/reference/pli/ms/vinaya/pli-tv-pvr/pli-tv-pvr{chapter}_reference.json"

    insert_csv = f"../daff-fun/{insert_csv}"

    # Do the insert!
    insert_refs(root_ref_json, insert_csv, root_ref_json)
