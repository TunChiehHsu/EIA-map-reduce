#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import sqlite3
from itertools import imap

TABLE_SCHEMA = (
    'CREATE TABLE EDGES('
    'src INT,'
    'trg INT,'
    'PRIMARY KEY (src, trg)'
    ');'
)

def search(node, db_path='edges.db'):
     with sqlite3.connect(db_path) as conn:
         cur = conn.cursor()
         cmd = 'SELECT src, trg FROM EDGES WHERE trg=?'
         for res in cur.execute(cmd, (node,)):
             yield res

def init_edge_db(edges, db_path='edges.db'):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS EDGES;")
        # create table
        cur.execute(TABLE_SCHEMA)
        # insert data
        cur.executemany('INSERT INTO EDGES VALUES (?, ?)', edges)


if __name__ == '__main__':
    edges = imap(lambda x: x.strip().split(','), fileinput.input())
    init_edge_db(edges)
