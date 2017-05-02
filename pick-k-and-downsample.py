#! /usr/bin/env python
from __future__ import print_function
import sys
import sourmash_lib
from sourmash_lib import signature
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument('sigfile')
    p.add_argument('-k', '--ksize', default=31)
    p.add_argument('--scaled', default=10000, type=int)
    args = p.parse_args()

    sigs = list(signature.load_signatures(args.sigfile))
    print('loaded {} signatures'.format(len(sigs)), file=sys.stderr)

    found = None
    for sig in sigs:
        if sig.minhash.ksize == args.ksize:
            found = sig
            break

    if not found:
        print('no such sig found', file=sys.stderr)
        sys.exit(0)

    found.minhash = found.minhash.downsample_scaled(args.scaled)

    signature.save_signatures([found], sys.stdout)


if __name__ == '__main__':
    main()
