#! /usr/bin/env python
import argparse
import collections
import sourmash_lib.signature
import numpy


def main():
    p = argparse.ArgumentParser()
    p.add_argument('inp_signatures', nargs='+')
    args = p.parse_args()

    counts = collections.Counter()

    print('loading signatures from', len(args.inp_signatures), 'files')
    for filename in args.inp_signatures:
        sig = sourmash_lib.signature.load_one_signature(filename)
        mh = sig.minhash
        hashes = mh.get_mins()

        for k in hashes:
            counts[k] += 1

    [(highest, count)] = counts.most_common(1)
    print("most common hash is {} and has a count of {}".format(highest, count))

    save_list = []
    for filename in args.inp_signatures:
        sig = sourmash_lib.signature.load_one_signature(filename)
        mh = sig.minhash
        hashes = mh.get_mins()

        if highest in hashes:
            save_list.append(sig.name())

    with open('savelist.txt', 'w') as fp:
        fp.write("\n".join(save_list))

if __name__ == '__main__':
    main()
