#!/usr/bin/env python3

from contextlib import redirect_stdout
from datetime import datetime
import os
import subprocess

## Set up directories and filenames.
CWD = os.getcwd()
VINAYA_PATH = "/home/nadi/Development/sc/bilara-data/translation/en/brahmali/vinaya"

title_segments_files = [
        "titles-bi.csv",
        "titles-bu.csv",
        "titles-kd.csv",
        "titles-pvr.csv"
        ]


def get_segment_text(segment_id):
    """
    Return the translation text given a segment ID.
    Assumes segment_id includes surrounding quotes.
    """
    os.chdir(VINAYA_PATH)
    output = subprocess.run(["ag", f'{segment_id}:', "--nofilename"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    os.chdir(CWD)

    # The line should be something like
    #   "seg_id": "text ",
    # We just want the text bit.
    # And we want to take out that trailing space.
    if output:
        text = output.split(": ", 1)[1].rstrip(",").strip('"').strip()
    else:
        text = ""
    return text


def generate(segment_file):
    """
    Generate a csv file with doc id, title segment id, title text.
    """
    with open(segment_file) as csv_file:
        for line in csv_file:
            sid = line.strip().strip('"')
            generate_line(sid)

def generate_line(sid):
    # Get the document id, sort of.
    uid = sid[:sid.find(":")]
    # Exceptions!
    if uid == "pli-tv-bu-vb-as1":
        uid = "pli-tv-bu-vb-as1-7"
    elif uid == "pli-tv-bi-vb-as1":
        uid = "pli-tv-bi-vb-as1-7"
    elif uid == "pli-tv-bi-vb-pj1":
        uid = "pli-tv-bi-vb-pj1-4"
    elif uid == "pli-tv-bi-pc91":
        uid = "pli-tv-bi-pc91-93"
    elif uid == "pli-tv-bi-vb-pd2":
        uid == "pli-tv-bi-vb-pd2-8"

    key = f"{uid}_en"

    # Get the text for the segments.
    segment_text = get_segment_text(f'"{sid}"')

    print(f'"{uid}","{key}","{sid}","{segment_text}"')


# Run!

timestamp = datetime.now().strftime("%y%m%d-%H%M%S")
outfile_name = f"{timestamp}-all-titles.txt"

with open(outfile_name, 'w') as f:
    with redirect_stdout(f):
        for csv_file in title_segments_files:
            generate(csv_file)
