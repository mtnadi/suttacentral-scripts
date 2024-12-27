#!/usr/bin/env python3

import difflib
import os
import subprocess

## Set up directories and filenames.
CWD = os.getcwd()
VINAYA_PATH = "/home/nadi/Development/sc/bilara-data/translation/en/brahmali/vinaya"
# TODO bu pc 31 and 49 are borken

bi_pm_file = f"{VINAYA_PATH}/pli-tv-bi-pm_translation-en-brahmali.json"
bu_pm_file = f"{VINAYA_PATH}/pli-tv-bu-pm_translation-en-brahmali.json"

bi_pm_vb_segments_file = "pm-to-vb-bi.csv"
bu_pm_vb_segments_file = "pm-to-vb-bu.csv"


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


# ohhhh the bad programming...!
bu_classes = [
    ("Expulsion", 4),
    ("Suspension", 13),
    ("Undetermined", 2),
    ("Relinquishment and confession", 30),
    ("Confession", 92),
    ("Acknowledgement", 4),
    ("Training", 75),
    ("The settling of legal issues", 7)
    ]
bi_classes = [
    ("Expulsion", 8),
    ("Suspension", 17),
    ("Relinquishment and confession", 30),
    ("Confession", 166),
    ("Acknowledgement", 8),
    ("Training", 75),
    ("The settling of legal issues", 7)
    ]
class_index = 0
rule_number = 1

def compare(key_file, monks_or_nuns, pm_or_vb):
    """
    For each line in the key csv file, check that the segments have the same text,
    or if it is not a vb segment ID, check that the heading is in order.
    """
    with open(key_file) as csv_file:
        for line in csv_file:
            [pm_sid, vb_sid] = line.strip().split(",",1)
            check_line(pm_sid, vb_sid, monks_or_nuns, pm_or_vb)

def check_line(pm_sid, vb_sid, monks_or_nuns, pm_or_vb):
    global class_index
    global rule_number

    # Get rule classes.
    if monks_or_nuns == "bu":
        rule_classes = bu_classes
    else:
        rule_classes = bi_classes

    # Get the text for the pm entry.
    pm_stext = get_translation_text(pm_sid)

    # Check whether the second entry is a segment ID.  If it's not, it will
    # happen to be the text of the pm file at time of creation, but that's not
    # useful so don't depend on it.
    vb_stext = "SKIP"
    if "pli-tv-" in vb_sid:
        # Get the text for the segments.
        vb_stext = get_translation_text(vb_sid)

        # If we're looking at the bi-pm, then if the vb text points to
        # something in pli-tv-bu, then substitute monk/he/him
        if monks_or_nuns == "bi" and "pli-tv-bu-" in vb_sid:
            vb_stext = vb_stext.replace("monk", "nun")
            vb_stext = vb_stext.replace(" he ", " she ")
            vb_stext = vb_stext.replace("He ", "She ")
            vb_stext = vb_stext.replace('"he ', '"she ')
            vb_stext = vb_stext.replace(" him", " her")
            vb_stext = vb_stext.replace(" his ", " her ")
    else:
        # Skip checking the Recitation of blah segments.
        # Also skip checking (sub)chapter on blah is finished segments.
        # Left them in the CSV
        # data in case we later want to check it against the vb text.
        if "ecitation" not in vb_sid and "hapter" not in vb_sid and "nid:" not in vb_sid:
            vb_sid = "rule title, checking it's in order:"

            # Check whether the rule title has the right number.
            if rule_classes[class_index][0] in pm_stext and str(rule_number) in pm_stext:
                vb_stext = "yay!"
            else:
                vb_stext = f"UH OH!  Rule name is wonky.  Expected {rule_classes[class_index][0]} {str(rule_number)} in it."

            # Update indices.
            rule_number += 1
            if rule_number > rule_classes[class_index][1]:
                class_index += 1
                rule_number = 1

    if vb_stext not in ["SKIP", "yay!"]:
        if pm_or_vb == "pm":
            # print out pm segment ids and text on alternate lines to use with diff
            if vb_sid.startswith("rule title, checking"):
                vb_sid = ""
            print(f"{vb_sid}>{pm_sid}")
            print(f"{pm_stext}")
        else:
            # print out vb segment ids and text on alternate lines to use with diff
            if vb_sid.startswith("rule title, checking"):
                vb_sid = pm_sid
            if vb_stext.startswith("yay") or vb_stext.startswith("UH OH"):
                vb_stext = pm_stext
            print(f"{vb_sid}<{pm_sid}")
            print(f"{vb_stext}")


# Run!
#compare(bu_pm_vb_segments_file, "bu", "pm")
#compare(bu_pm_vb_segments_file, "bu", "vb")

#compare(bi_pm_vb_segments_file, "bi", "pm")
compare(bi_pm_vb_segments_file, "bi", "vb")
