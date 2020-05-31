#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="flag missing or duplicate references")
parser.add_argument("filename", help="The text file to process of results from command line; best to cat reference files into one file but must be >>'d in order.")
args = parser.parse_args()

text = ""
with open(args.filename) as f:
    for line in f:
        text += line

# get bj prefix (with volume)
def get_bj_prefix(text):
    b_ind = text.index("bj")
    dot_ind = text.index(".", b_ind)
    return text[b_ind:dot_ind+1]

# get ms prefix
def get_ms_prefix(text):
    m_ind = text.index("ms")
    und_ind = text.index("_", m_ind)
    return text[m_ind:und_ind+1]

def get_pts_prefix(text, ed):
    if ed:
        pref = f"pts-vp-pli{ed}ed"
    else:
        pref = "pts-vp-pli"
    p_ind = text.index(pref)
    try:
        dot_ind = text.index(".", p_ind)
        com_ind = text.index(",", p_ind)
        if com_ind < dot_ind:
            raise RuntimeError
    except:
        dot_ind = p_ind + len(pref) - 1
    return text[p_ind:dot_ind + 1]

# get pts 1ed prefix - may or may not have volume number
def get_pts1_prefix(text):
    return get_pts_prefix(text, "1")

# get pts 2ed prefix - may or may not have volume number
def get_pts2_prefix(text):
    return get_pts_prefix(text, "2")

def get_pts_no_ed_prefix(text):
    return get_pts_prefix(text, "")

# get first and last reference
def get_min_max_ref(text, prefix):
    first_ind = text.index(prefix)

    # usually the reference ends with a comma, but sometimes with "
    first_end_ind = text.index('"', first_ind)
    com_ind = text.index(",", first_ind)
    first_end_ind = min(first_end_ind, com_ind)

    first_ref = text[first_ind + len(prefix):first_end_ind]

    last_ind = text.rfind(prefix)
    try:
        # if we're looking at the last element of the JSON object, there won't be a ,
        last_end_ind = text.index(",", last_ind)
    except ValueError:
        last_end_ind = text.index('"', last_ind)
    last_ref = text[last_ind + len(prefix) : last_end_ind]
    # debugging print(f"prefix {prefix} first {first_ref} last {last_ref}")
    return [int(first_ref), int(last_ref)]

# loop over all references and alert when count is off
# first and last must be integers
# returns whether there were errors
def check_ref_range(text, prefix, first, last):
    has_errs = False
    last_index = 0
    for ref in range(first, last + 1):
        # bj references only have even numbered pages
        if prefix.startswith("bj") and ref % 2 == 1:
            continue
        search_string = prefix + str(ref) + ","
        occ = text.count(search_string)
        occ_ind = text.find(search_string)
        if occ < 1:
            # check whether it just appears at the end of the line
            search_string = prefix + str(ref) + '"'
            occ = text.count(search_string)
            occ_ind = text.find(search_string)

        if occ < 1:
            print(f"Missing {prefix + str(ref)}")
            has_errs = True
        elif occ > 1:
            print(f"{occ} occurences of {prefix + str(ref)}")
            has_errs = True
        else:
            if occ_ind < last_index:
                print(f"{prefix + str(ref)} appears before the previous reference (assuming no duplicates)")
                has_errs = True
        last_index = occ_ind
    return has_errs


def check(text, prefix):
    [first, last] = get_min_max_ref(text, prefix)
    print(f"***Check {prefix} {first}-{last}")
    if not check_ref_range(text, prefix, first, last):
        print("Okay")

check(text, get_bj_prefix(text))
try:
    check(text, get_pts1_prefix(text))
    check(text, get_pts2_prefix(text))
except ValueError:
    check(text, get_pts_no_ed_prefix(text))
check(text, get_ms_prefix(text))
