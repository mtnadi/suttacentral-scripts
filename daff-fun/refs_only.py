#!/usr/local/opt/python@3.8/bin/python3
import csv

# Files!
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
for input_file in files:
    print(f"...Processing {input_file}...")

    assert input_file[:3] == "ref" and input_file[-4:] == ".csv", "Funky filename.  Expected filename ref[blah].csv"

    # Run through csv and pull out references with their segments.
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

    import pprint; pprint.pprint(references)
