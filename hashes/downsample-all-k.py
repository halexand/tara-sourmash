#! /usr/bin/env python
from __future__ import print_function
import sys
import sourmash_lib
from sourmash_lib import signature
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument('sigfile')
    p.add_argument('--scaled', default=10000, type=int)

    args = p.parse_args()

    sigs = list(signature.load_signatures(args.sigfile))
    print('loaded {} signatures'.format(len(sigs)), file=sys.stderr)

    outsigs=[]
    for sig in sigs:
        sig.minhash = sig.minhash.downsample_scaled(args.scaled)
        outsigs.append(sig)

    signature.save_signatures(outsigs, sys.stdout)


if __name__ == '__main__':
    main()
