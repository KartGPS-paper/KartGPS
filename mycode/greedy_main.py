#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : hxinaa
from sys import argv
import match
import graph

def greedy(g,R,B=10):
    maxu = 0
    for r1 in R:
        for r2 in R:
            for r3 in R:
                if r1!=r2 and r2!=r3 and r3!=r1:
                    total_cost = r1.cost+r2.cost+r3.cost

                    if total_cost <= B:
                        selected = [r1,r2,r3]
                        totalU = match.utility(selected)
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
                            totalU = match.utility(selected)
                    if totalU> maxu:
                        totalU = maxu
                        ans = selected
    return ans,maxu


if __name__ == '__main__':
    print("main")