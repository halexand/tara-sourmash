#! /usr/bin/env python
"""
Given a list of read files output by (e.g.) find-hashes-2.py, this
script will extract all of the reads that are present in all of those
read files (intersection of read files).

It does this by filtering the collection of reads against a Bloom filter
created from each read data set, using median k-mer abundance to decide
on presence/absence.
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

    remove_queue = [None, None]
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

        n = 0
        m = 0
        for n, record in enumerate(clean_input_reads(screed.open(inputfile))):
            if len(record.sequence) < K:
                continue

            if kh.median_at_least(record.cleaned_seq, 1):
                khmer.utils.write_record(record, fp)
                m += 1
        fp.close()
        print('read {}, wrote {}'.format(n, m))

        if inputfile.startswith(BASE):
            remove_queue.append(inputfile)
        remove_name = remove_queue.pop(0)
        if remove_name:
            print('removing', remove_name)
            os.unlink(remove_name)
        
        inputfile = outputfile

    print('final file is:', inputfile)
    

if __name__ == '__main__':
    main()
