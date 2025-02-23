#!/usr/bin/env python3

import csv

# old stuff:
from contextlib import redirect_stdout

name_files = [
        "pli-tv-bi-pm-name_translation-en-sujato.json",
        "pli-tv-bi-vb-name_translation-en-sujato.json",
        "pli-tv-bu-pm-name_translation-en-sujato.json",
        "pli-tv-bu-vb-name_translation-en-sujato.json",
        "pli-tv-kd-name_translation-en-sujato.json",
        "pli-tv-pvr-name_translation-en-sujato.json"
        ]


def import_new_titles():
    """
    Take titles csv files and creates a dict of uid:title.
    """
    title_files = [
            "titles-trans.csv",
            "titles-notrans.csv"
            ]
    titles_by_uid = {}
    for f in title_files:
        with open(f, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            for (uid, title) in reader:
                assert uid not in titles_by_uid, f"DUPLICATE UID: {uid}:\n  {titles_by_uid[uid]}\n  {title}"
                titles_by_uid[uid] = title
    return titles_by_uid


def process_name_file(filename, titles_by_uid):
    """
    Read in a name .json file and output a new file with updated titles.
    """
    with open(filename, "r") as f:
        for l in f:
            line = l.strip()
            if line == "{" or line == "}":
                print(line)
            else:
                # line format:`  "segment id": "title ",`
                # The last line doesn't have trailing comma.
                # Extract the segment id and existing title.
                append_comma = "," if line.endswith(",") else ""
                line = line.strip(",").strip('"').strip()
                (segment_id, _, existing_title) = line.partition('": "')

                # segment_id format:`pli-tv-<book>-name:<n>.<uid>`
                # We just need the uid to get the new title.
                uid = segment_id[segment_id.index(".") + 1:]
                # If this is a bi-pm or bu-pm uid, get the corresponding
                # bi-vb or bu-vb title.
                if uid.startswith("pli-tv-bi-pm"):
                    uid = f"pli-tv-bi-vb-{uid[13:]}"
                elif uid.startswith("pli-tv-bu-pm"):
                    uid = f"pli-tv-bu-vb-{uid[13:]}"
                out_title = titles_by_uid.get(uid, existing_title)

                # Spit line back out with the new title.
                print(f'  "{segment_id}": "{out_title} "{append_comma}')


# Run!
title_dict = import_new_titles()
for name_file in name_files:
    outfile_name = f"new-{name_file}"
    with open(outfile_name, 'w') as f:
        with redirect_stdout(f):
            process_name_file(name_file, title_dict)
