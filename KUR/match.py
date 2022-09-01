#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-04-21 20:57
# @Author  : hxinaa
from sys import argv
import graph
import copy
import pandas as pd
import time
from random import *
import math

def utility(R):
    return total_cover(R).shape[0]

def total_cover(R):
    ans = R[0].getcover()
    for ri in range(1,len(R)):
        ans = set_union(ans,R[ri].getcover())
    return ans


class Rule:
    def __init__(self,pattern,headid):
        self.query = pattern
        self.target = headid
        self.cover = pd.DataFrame([])
        self.conf = -1

    def cost(self):
        return 1

    def getcover(self,graph):
        if self.cover.shape[0]>0:
            return self.cover
        self.cover = match(graph,self.query,self.target)
        return self.cover

    def getconfident(self,graph,F):
        if self.conf > -1:
            return self.cover
        self.conf = confident(F,graph,self.query,self.target)
        return self.conf

    def deltaU(self,selected):
        ans = total_cover(selected)
        diff = set_diff(set_union(ans,self.cover),ans)
        return diff.shape[0]

def get_candidate(g,query,e):
    """

    :param g:
    :param query:
    :param e:
    :return: pd [efrm,eto] in g
    """
    l1 = []
    l2 = []
    evlb1 = query.vertices[e.frm].vlb
    evlb2 = query.vertices[e.to].vlb
    print(evlb1,evlb2)
    print("candidate:",e)
    print("same label in g:",g.set_of_elb)
    for eid in g.set_of_elb[e.elb]:
        ei = g.all_edges[eid]
        if g.vertices[ei.frm].vlb==evlb1 and g.vertices[ei.to].vlb==evlb2:
            l1.append(ei.frm)
            l2.append(ei.to)
    ans = pd.DataFrame({e.frm:l1,e.to:l2})
    print("candidate ans:",ans)
    return ans

# input: query, graph, F
# target: edge pattern
# output: the part of F can be coverd by query

def join(t1,t2):
    # print("join table1:",t1)
    # print("join table2:",t2)
    # print("node:",node)
    # print("**"*10)
    cols = list(set(t1.columns) & set(t2.columns))
    # print(cols)
    ans = pd.merge(t1,t2,on=cols,how='inner')
    # print(ans)
    # print("==" * 10)
    return ans

def set_inner(d1,d2):
    # print(d1.columns)
    # print(list(d2.columns))
    # print("d1 data:",d1)
    # print("size:",d1.shape[0])
    return pd.merge(d1,d2,on=list(d1.columns),how='inner')

def set_diff(d1,d2):
    # d1-d2
    return pd.concat([d1,d2,d2]).drop_duplicates(keep=False)

def set_union(d1,d2):
    return pd.merge(d1,d2,on=list(d1.columns),how='outer')





def match(graph,query,target):
    """

    :param F:
    :param graph:
    :param query:
    :param target:
    :return: pd: [efrm,eto]
    """
    candidate = {}
    flag = {}
    qedge_dict = query.get_all_edges()

    # print(qedge_dict)
    for eid in qedge_dict.keys():
        e = qedge_dict[eid]
        candidate[eid] = get_candidate(graph,query,e)
        flag[eid] = True

    # print("after:",ans)
    ans = candidate[target]

    target_node = ans.columns
    # print("nodelist:",target_node)

    # ans = pd.merge(ans,F,how='inner')
    flag[target] = False
    # for e in graph.elbdict[target.lb]:
    #     if e.id in F:
    #         candidate[target].append(e)
    nodelist = [qedge_dict[target].frm,qedge_dict[target].to]
    for node in nodelist:
        edges = query.roundedges[node]
        print("flag:",flag)
        for eid in edges:
            if flag[eid]:
                ans = join(ans,candidate[eid])
                flag[eid] = False
                e = qedge_dict[eid]
                if e.frm==node and e.to not in set(nodelist):
                    nodelist.append(e.to)
                if e.to==node and e.frm not in set(nodelist):
                    nodelist.append(e.frm)

    return ans[target_node]


def confident(F,graph,query,target):
    covered_fact = match(graph,query,target)
    ans = set_inner(covered_fact,F)
    conf = ans.shape[0]/F.shape[0]
    return conf


def test():
    g = graph.read_graphs("graph.data.1")[0]
    Body = graph.Graph(-1, eid_auto_increment=True)
    Body.add_vertex('1', '1')
    Body.add_vertex('2', '2')
    Body.add_vertex('3', '3')

    Body.add_edge(-1, '1', '2', '1')
    Body.add_edge(-1, '1', '3', '1')
    Body.add_edge(-1, '2', '3', '1')

    rule = Rule(Body, 1)
    F = pd.DataFrame({'1':['1','4','7'],'3':['3','3','5']})
    print(rule.getcover(g))
    print(rule.getconfident(g,F))

if __name__ == '__main__':

    test()
    # g = graph.read_graphs("graph.data.1")[0]
    # print("-----")
    # pattern = graph.read_graphs("query_graph.1")[0]
    #
    # target = 1
    # facts = g.get_all_edges()
    # pattern.display()
    # print(pattern.get_all_edges())
    # print("*"*10)
    # qedge_dict = pattern.get_all_edges()
    # target_e = qedge_dict[target]
    # facts = get_candidate(g,pattern,target_e)
    # print("facts:",facts)
    #
    # ans = cover(facts,g,pattern,target)

