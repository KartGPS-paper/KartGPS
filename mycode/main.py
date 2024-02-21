#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : hxinaa
from sys import argv
import xingraph as graph
import codecs
import collections
from rdflib import Graph,URIRef
import numpy as np

def read_graphs_from_file(file_name,_is_undirected):
    graphs = dict()
    with codecs.open(file_name, 'r', 'utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        tgraph, graph_cnt = None, 0
        for i, line in enumerate(lines):
            cols = line.split(' ')
            if cols[0] == 't':
                if tgraph is not None:
                    graphs[graph_cnt] = tgraph
                    graph_cnt += 1
                    tgraph = None

                tgraph = graph.Graph(graph_cnt,
                               is_undirected=_is_undirected,
                               eid_auto_increment=True)
            elif cols[0] == 'v':
                tgraph.add_vertex(cols[1], cols[2])
            elif cols[0] == 'e':
                # print(cols)
                tgraph.add_edge(0,cols[1], cols[2], cols[3])
        # adapt to input files that do not end with 't # -1'
        if tgraph is not None:
            graphs[graph_cnt] = tgraph
        return graphs

def generate_1edge_frequent_subgraphs(graphs,min_support):
    vlb_counter = collections.Counter()
    vevlb_counter = collections.Counter()
    vlb_counted = set()
    vevlb_counted = set()
    frequent_size1_subgraphs = []
    for g in graphs.values():
        for v in g.vertices.values():
            if (g.gid, v.vlb) not in vlb_counted:
                vlb_counter[v.vlb] += 1
            vlb_counted.add((g.gid, v.vlb))
            for to, e in v.edges.items():
                vlb1, vlb2 = v.vlb, g.vertices[to].vlb
                if g.is_undirected and vlb1 > vlb2:
                    vlb1, vlb2 = vlb2, vlb1
                if (g.gid, (vlb1, e.elb, vlb2)) not in vevlb_counter:
                    vevlb_counter[(vlb1, e.elb, vlb2)] += 1
                vevlb_counted.add((g.gid, (vlb1, e.elb, vlb2)))
    # add frequent vertices.
    for vlb, cnt in vlb_counter.items():
        if cnt >= min_support:
            g = graph.Graph(gid=next(self._counter),
                      is_undirected=self._is_undirected)
            g.add_vertex(0, vlb)
            frequent_size1_subgraphs.append(g)
            if self._min_num_vertices <= 1:
                self._report_size1(g, support=cnt)
        else:
            continue
    if self._min_num_vertices > 1:
        self._counter = itertools.count()


def utility(L,F):
    return 0

def greedy(g,conf,B,R):
    maxu = 0
    for r1 in R:
        for r2 in R:
            for r3 in R:
                if r1!=r2 and r2!=r3 and r3!=r1:
                    total_cost = r1.cost+r2.cost+r3.cost

                    if total_cost <= B:
                        selected = [r1,r2,r3]
                        totalU = utility(selected)
                        candidate = list(set(R)-set([r1,r2,r3]))
                        while len(candidate)>0 and total_cost<=B:
                            maxscore = -1
                            for r4 in R:
                                if r4.deltaU(selected)/r4.cost>maxscore:
                                    maxscore = r4.deltaU(selected)/r4.cost
                                    maxr = r4
                            if maxscore>0 and total_cost+maxr.cost<=B:
                                selected.append(maxr)
                            candidate = list(set(candidate)-set([maxr]))
                            totalU = utility(selected)
                    if totalU> maxu:
                        totalU = maxu
                        ans = selected
    return ans,maxu

def test():
    g = read_graphs_from_file("graph.data.directed.1", True)[0]
    gs = graph.gSpan(
        database_file_name="graph.data.directed.1",
        min_support=1,
        min_num_vertices=1,
        max_num_vertices=10,
        max_ngraphs=10,
        is_undirected=False,
        verbose=True,
        visualize=False,
        where=False
    )

if __name__ == '__main__':

    data = np.array([[0, 0, 0, 0], [0, 1, 1, 1], [0, 2, 2, 2], [0, 3, 3, 3], [4, 0, 5, 0], [4, 1, 6, 1], [4, 2, 7, 2],
                     [4, 3, 8, 3], [1,0,5,0],[1,1,6,1],[1,2,7,2]])
    g = Graph()

    for x in data:
        g.add((URIRef('http://'+str(x[0])),URIRef('http://rel'+str(x[1])+str(x[3])),URIRef('http://'+str(x[2]))))
    for x in g.triples((None, None, None)):
        print(x)

    q = "select ?x where { ?x <http://rel00> ?o1. ?x <http://rel11> ?o2. ?x <http://rel22> ?o3. ?x <http://rel33> ?o4.}"
    q2 = "select ?x where { ?x <http://rel00> ?o1. ?x <http://rel11> ?o2. ?x <http://rel22> ?o3.}"
    x = g.query(q)
    print(list(x))
    x = g.query(q2)
    print(list(x))




