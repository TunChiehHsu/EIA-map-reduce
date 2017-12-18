#!/usr/bin/env python
# -*- coding: utf-8 -*-

# cat ngm.test.txt | python pg-map.py | sort | python pg-reduce.py > temp.txt
# rm -r result ; time zcat aw.gen.ngm-all.gz | ./lmr 500m 16 'python
# test-map.py' 'python test-reduce.py' result

import fileinput
from itertools import groupby, imap, product
from operator import itemgetter


def parse(line):
    key, path = line.strip().split('\t')
    key = tuple(map(int, key.split()))
    # key = tuple(key.split())
    path = tuple(map(int, path.split(',')))
    # path = tuple(path.split(','))
    return key, path

if __name__ == '__main__':
    input_iterator = imap(parse, fileinput.input())
    for key, values in groupby(input_iterator, itemgetter(0)):
        head, connect = key
        paths = map(itemgetter(1), values)
        th, tl = set(), set()
        for path in paths:
            if path[0] == head:
                th.add(path)
            else:
                tl.add(path)
        for tf, tr in product(th, tl):
            if not any(node in tf for node in tr[1:-1]):
                print ','.join(map(str, tf + tr[1:]))
