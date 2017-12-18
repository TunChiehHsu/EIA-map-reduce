#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import sqlite3
from itertools import groupby, imap, product
from operator import itemgetter


def parse(line):
    key, path = line.strip().split('\t')
    key = int(key)
    path = tuple(map(int, path.split(',')))
    # path = tuple(path.split(','))
    return key, path


def search(node, db_path='edges.db'):
     with sqlite3.connect(db_path) as conn:
         cur = conn.cursor()
         cmd = 'SELECT src FROM EDGES WHERE trg=?'
         for res in cur.execute(cmd, (node,)):
             yield res

if __name__ == '__main__':
    input_iterator = imap(parse, fileinput.input())
    for key, inputs in groupby(input_iterator, itemgetter(0)):
        extend = set(search(key))
        for _, path in inputs:
            for node in extend:
                if node > path[-1] and node not in path:
                    print ','.join(map(str, (node) + path))
        del extend
        del inputs
