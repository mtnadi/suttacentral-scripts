#!/usr/bin/env python3

import os
import subprocess

cwd = os.getcwd()
key_file = "key.csv"
kd18_translation_file = "/Users/tracy/Development/bilara-data/translation/en/brahmali/vinaya/pli-tv-kd/pli-tv-kd18_translation-en-brahmali.json"
kd_dir = "/Users/tracy/Development/bilara-data/translation/en/brahmali/vinaya/pli-tv-kd"
bu_sk_dir = "/Users/tracy/Development/bilara-data/translation/en/brahmali/vinaya/pli-tv-bu-vb/pli-tv-bu-vb-sk"

def get_sk_rule(segment_id):
    os.chdir(bu_sk_dir)
    output = subprocess.run(["ag", f'"{segment_id}":', "--nofilename"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    os.chdir(cwd)
    return output[output.find('‘')+1:output.rfind('’')]

def get_kd18_text(segment_id):
    os.chdir(kd_dir)
    output = subprocess.run(["ag", f'"{segment_id}":', "--nofilename"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    os.chdir(cwd)
    return output

with open(key_file) as csv_file:
    for line in csv_file:
        [kd18_seg_id, sk_seg_id] = line.strip().split(",")
        print(f"{sk_seg_id: <26}{get_sk_rule(sk_seg_id)}")
        print(f"{get_kd18_text(kd18_seg_id)}\n")
