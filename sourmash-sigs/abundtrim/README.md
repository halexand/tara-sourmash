# Hash foo for multisample extraction fiz

See:

[find-hashes.py](./find-hashes.py)

[find-hashes-2.py](./find-hashes-2.py)

[cluster-samples-by-hash.ipynb](./cluster-samples-by-hash.ipynb)

[collect-reads.py](./collect-reads.py)

[collect-reads-2.py](./collect-reads-2.py)

# Notes

Intersection-based approaches like the one used in collect-reads
eliminate a lot of reads very quickly; see below.  So in practice we
probably don't need to iterate over all the files unless we want to
boost coverage by extracting all the reads from all the files (see
[collect-reads-2.py](./collect-reads-2.py)).

```
starting with ERR599173_1.head.paired.fq.gz.abundtrim.gz
loading kh: ERR315858_1.head.paired.fq.gz.abundtrim.gz
iterating over reads: ERR599173_1.head.paired.fq.gz.abundtrim.gz
read 294698, wrote 18590
loading kh: ERR315861_1.head.paired.fq.gz.abundtrim.gz
iterating over reads: COLLECTING.fq.0
read 18589, wrote 12620
loading kh: ERR318618_1.head.paired.fq.gz.abundtrim.gz
iterating over reads: COLLECTING.fq.1
read 12619, wrote 9522
removing COLLECTING.fq.0
loading kh: ERR318619_1.head.paired.fq.gz.abundtrim.gz
iterating over reads: COLLECTING.fq.2
read 9521, wrote 7091
removing COLLECTING.fq.1
loading kh: ERR318620_1.head.paired.fq.gz.abundtrim.gz
iterating over reads: COLLECTING.fq.3
read 7090, wrote 6584
removing COLLECTING.fq.2
loading kh: ERR598943_1.head.paired.fq.gz.abundtrim.gz
iterating over reads: COLLECTING.fq.4
read 6583, wrote 5134
removing COLLECTING.fq.3
loading kh: ERR598946_1.head.paired.fq.gz.abundtrim.gz
iterating over reads: COLLECTING.fq.5
read 5133, wrote 2668
removing COLLECTING.fq.4
...
```
