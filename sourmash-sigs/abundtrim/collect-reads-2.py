#! /usr/bin/env python
"""
Given a list of read files output by (e.g.) find-hashes-2.py, this
script will extract all of the reads that are present in all of those
read files (intersection of read files).

This script modifies the approach in collect-reads.py to collect reads
from all the files, vs collecting the reads from sample 1 that are in
all the other files.
"""
from __future__ import print_function
import os

import khmer
import argparse
import screed
from khmer.utils import clean_input_reads


BASE = 'COLLECTING.fq'


DIRECTORY='/mnt/home/ctb/tara-sourmash/harriet-reads'
K = 21


def main():
    p = argparse.ArgumentParser()
    p.add_argument('readfilelist')
    args = p.parse_args()

    filelist = open(args.readfilelist).readlines()
    filelist = [ x.strip() for x in filelist ]

    inputfile = filelist.pop()
    while not os.path.exists(inputfile):
        inputfile = filelist.pop()
    print('starting with', inputfile)

    collected = 0
    for pos, filename in enumerate(filelist):
        if not os.path.exists(filename):
            print('skipping', filename)
            continue

        print('loading kh:', filename)
        kh = khmer.Nodetable(K, 2e8, 4)
        kh.consume_seqfile(filename)

        print('iterating over reads:', inputfile)

        outputfile = BASE + '.{}'.format(pos)
        fp = open(outputfile, 'w')

        m = 0
        for n, record in enumerate(clean_input_reads(screed.open(inputfile))):
            if len(record.sequence) < K:
                continue

            if kh.median_at_least(record.cleaned_seq, 1):
                khmer.utils.write_record(record, fp)
                m += 1
        fp.close()
        print('read {}, wrote {}'.format(n, m))

        inputfile = outputfile
        collected += 1

        if collected > 5:
            break

    # second round: load results of first round into bloom filter,
    # use that to sweep reads out of all the files.

    kh = khmer.Nodetable(K, 2e7, 4)
    kh.consume_seqfile(inputfile)

    filelist = open(args.readfilelist).readlines()
    filelist = [ x.strip() for x in filelist ]

    total_read = 0
    total_written = 0
    for n, filename in enumerate(filelist):
        print('reading', n, filename)
        if not os.path.exists(filename):
            continue
        fp = open(os.path.basename(filename) + '.collected', 'w')

        m = 0
        for n, record in enumerate(clean_input_reads(screed.open(filename))):
            if len(record.sequence) < K:
                continue
            if kh.median_at_least(record.cleaned_seq, 1):
                khmer.utils.write_record(record, fp)
                m += 1
        fp.close()
        print('read {}, wrote {}'.format(n, m))
        total_read += n
        total_written += m
        print('total so far:', total_read, total_written)

    print('Results are in *.collected.')

if __name__ == '__main__':
    main()
