#!/usr/bin/env python3
from json import load
from glob import glob
import re

# regex to extract tags from sublime settings files #
ts = re.compile(r'(.*)\t(.*): (.*) .*')

# scan subdirectories to get tag files #
for folder in glob('*/'):
    geany_tags = []

    # load sublime settings json files from the folder #
    search_pattern = folder+'*.sublime-settings'
    for json_file in glob(search_pattern):
        print(f'processing {json_file}')
        with open(json_file) as stag_file:
            stags = load(stag_file)['completions']  # load tags from completions head
            for stag in stags:
                try:
                    # extract tags from the first array element stag[0] #
                    geany_tags.append(ts.search(stag[0]).groups())
                except Exception:
                    # if tag extraction fails for the standard definition try to extract just the keyword #
                    if re.search(r'(.*)\t.*', stag[0]):
                        geany_tags.append(re.search(r'(.*)\t.*', stag[0]).groups())

    print(f'processed {len(geany_tags)} tags')

    # create tags file name based on the folder name #
    gtag_filename = folder[:-1]+'.js.tags'
    with open(gtag_filename, 'w') as gtag_file:
        gtag_file.write('# format=pipe\n')
        # remove duplicate definitions using set #
        for tag in set(geany_tags):
            if len(tag) >= 3:
                gtag_file.write('{}|{}|{}|\n'.format(tag[0], tag[2], tag[1]))
            else:
                gtag_file.write('{}|||\n'.format(tag[0]))
