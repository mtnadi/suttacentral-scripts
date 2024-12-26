#!/usr/bin/env python3

import os
import subprocess

## Set up directories and filenames.
CWD = os.getcwd()
VINAYA_PATH = "/home/nadi/Development/sc/bilara-data/translation/en/brahmali/vinaya"

bi_pm_file = f"{VINAYA_PATH}/pli-tv-bi-pm_translation-en-brahmali.json"
bu_pm_file = f"{VINAYA_PATH}/pli-tv-bu-pm_translation-en-brahmali.json"

bi_pm_title_segments_file = "bi-rule-name.csv"
bu_pm_title_segments_file = "bu-rule-name.csv"


def make_segment_id_dict(csv_file):
    """
    Create a dictionary of pm title segment IDs to corresponding segment IDs.
    """
    lookup = {}
    f = open(file=csv_file)
    return lookup

def get_translation_text(segment_ref):
    if "," in segment_ref:
        text = '"'
        for sid in segment_ref.strip('"').split(","):
            text += get_segment_text(f'"{sid}"').strip('"')
        text += '"'
    else:
        text = get_segment_text(segment_ref)
    return text

def get_segment_text(segment_id):
    """
    Return the translation text given a segment ID.
    """
    os.chdir(VINAYA_PATH)
    output = subprocess.run(["ag", f'{segment_id}:', "--nofilename"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    os.chdir(CWD)

    # The line should be something like
    #   "seg_id": "text ",
    # We just want the text bit.
    if output:
        text = output.split(": ", 1)[1].rstrip(",")
    else:
        text = ""
    return text


def generate(key_file, monks_or_nuns, pm_or_ref):
    """
    Generate a text file with segment texts that can be run through a diff.
    """
    with open(key_file) as csv_file:
        for line in csv_file:
            [pm_sid, ref_sid] = line.strip().split(",",1)
            generate_line(pm_sid, ref_sid, monks_or_nuns, pm_or_ref)


def generate_line(pm_sid, ref_sid, monks_or_nuns, pm_or_ref):
    # Get the text for the pm entry.
    pm_stext = get_translation_text(pm_sid)

    # Get the text for the segments.
    ref_stext = get_translation_text(ref_sid)

    # If we're looking at the bi-pm, then if the ref text points to
    # something in pli-tv-bu, then substitute monk/he/him
    if monks_or_nuns == "bi" and "pli-tv-bu-" in ref_sid:
        ref_stext = ref_stext.replace("monk", "nun")
        ref_stext = ref_stext.replace(" he ", " she ")
        ref_stext = ref_stext.replace('"he ', '"she ')
        ref_stext = ref_stext.replace(" him", " her")
        ref_stext = ref_stext.replace(" his ", " her ")

    if pm_or_ref == "pm":
        # print out pm segment ids and text on alternate lines to use with diff
        print(f"{ref_sid}>{pm_sid}")
        print(f"{pm_stext}")
    else:
        # print out ref segment ids and text on alternate lines to use with diff
        print(f"{ref_sid}<{pm_sid}")
        print(f"{ref_stext}")


# Run!
#generate(bu_pm_title_segments_file, "bu", "pm")
generate(bu_pm_title_segments_file, "bu", "ref")
