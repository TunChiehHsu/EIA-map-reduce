#!/usr/bin/env python
# -*- coding: utf-8 -*-

# cat ngm.test.txt | python pg-map.py | sort | python pg-reduce.py > temp.txt
# rm -r result ; time zcat aw.gen.ngm-all.gz | ./lmr 500m 16 'python
# test-map.py' 'python test-reduce.py' result

import fileinput
import sys


if __name__ == '__main__':
    for line in fileinput.input():
        line = line.strip()
        path = map(int, line.split(','))
        # path = line.split(',')
        if path[0] < path[-1]:
            print >> sys.stdout, ','.join(map(str, path))
        else:
            print >> sys.stderr, ','.join(map(str, path))
