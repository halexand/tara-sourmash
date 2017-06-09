#! /usr/bin/env python
"""
Given a list of sourmash signatures, find the common hashes and
then output a file x hash matrix that can be used to cluster samples
by common hashes.
"""
from __future__ import print_function

import argparse
import collections
import sourmash_lib.signature
import numpy


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--min-samples', dest='min_samples', type=int)
    p.add_argument('inp_signatures', nargs='+')
    p.add_argument('-k', '--ksize', default = 21, type=int)
    args = p.parse_args()

    counts = collections.Counter()

    print('loading signatures from', len(args.inp_signatures), 'files')
    for filename in args.inp_signatures:
        sig = sourmash_lib.signature.load_one_signature(filename, select_ksize=args.ksize)
        mh = sig.minhash
        print(mh)
        hashes = mh.get_mins()

        for k in hashes:
            counts[k] += 1

    n = 0
    abundant_hashes = set()
    for hash, count in counts.most_common():
        if count < args.min_samples:
            break
        n += 1
        abundant_hashes.add(hash)

    print('found', n, 'hashes from', len(args.inp_signatures), 'signatures that had more than ', args.min_samples)

    # go over the files again, this time creating an n x n_files matrix
    # with 0 etc.
    pa = numpy.zeros((len(args.inp_signatures), len(abundant_hashes)),
                      dtype=numpy.int)

    # sort for no particular reason
    hashlist = list(sorted(abundant_hashes))
    hashdict = {}
    for n, k in enumerate(hashlist):
        hashdict[k] = n                   # hash -> index in hashlist

    for fn, filename in enumerate(args.inp_signatures):
        sig = sourmash_lib.signature.load_one_signature(filename, select_ksize=args.ksize)
        mh = sig.minhash
        hashes = mh.get_mins()

        x = abundant_hashes.intersection(hashes)
        for hashval in x:
            idx = hashdict[hashval]
            pa[fn][idx] = 1

    with open('mat', 'wb') as fp:
        numpy.save(fp, pa)

    with open('mat.labels.txt', 'w') as fp:
        fp.write("\n".join(args.inp_signatures))


if __name__ == '__main__':
    main()
