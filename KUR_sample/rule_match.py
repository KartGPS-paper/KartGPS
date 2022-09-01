#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : hxinaa
from sys import argv
import logging
from rdflib import Graph,URIRef
import numpy as np
def match(patten,kb):
    """

    :param patten: a list of constrains
    :param kb:
    :return instances: (dict) val mapping
    """

    patten_q = "select ?x,?y where "
    x = kb.query(patten_q)
    return list(x)

def test():
    data = np.array([[0, 0, 0, 0], [0, 1, 1, 1], [0, 2, 2, 2], [0, 3, 3, 3], [4, 0, 5, 0], [4, 1, 6, 1], [4, 2, 7, 2],
                     [4, 3, 8, 3], [1, 0, 5, 0], [1, 1, 6, 1], [1, 2, 7, 2]])
    g = Graph()

    for x in data:
        g.add((URIRef('http://' + str(x[0])), URIRef('http://rel' + str(x[1]) + str(x[3])),
               URIRef('http://' + str(x[2]))))
    for x in g.triples((None, None, None)):
        print(x)

    q = "select distinct ?x ?y where { ?x <http://rel00> ?o1. ?x <http://rel11> ?o2. ?x <http://rel22> ?o3. ?x <http://rel33> ?y.}"
    q2 = "select distinct ?x ?y where { ?x <http://rel00> ?o1. ?x <http://rel11> ?o2. ?x <http://rel22> ?o3. ?x ?rel ?y.}"
    ans = g.query(q)
    print(list(ans),len(ans))
    x = g.query(q2)
    print(list(x),len(x))
if __name__ == '__main__':
    print(test())