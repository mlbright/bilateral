#!/usr/bin/python
# Solution to http://www.spotify.com/us/jobs/tech/bilateral-projects/

import sys

## {{{ http://code.activestate.com/recipes/123641/ (r1)
# Hopcroft-Karp bipartite max-cardinality matching and max independent set
# David Eppstein, UC Irvine, 27 Apr 2002

def bipartiteMatch(graph):
    '''Find maximum cardinality matching of a bipartite graph (U,V,E).
    The input format is a dictionary mapping members of U to a list
    of their neighbors in V.  The output is a triple (M,A,B) where M is a
    dictionary mapping members of V to their matches in U, A is the part
    of the maximum independent set in U, and B is the part of the MIS in V.
    The same object may occur in both U and V, and is treated as two
    distinct vertices if this happens.'''
    
    # initialize greedy matching (redundant, but faster than full search)
    matching = {}
    for u in graph:
        for v in graph[u]:
            if v not in matching:
                matching[v] = u
                break
    
    while True:
        # structure residual graph into layers
        # pred[u] gives the neighbor in the previous layer for u in U
        # preds[v] gives a list of neighbors in the previous layer for v in V
        # unmatched gives a list of unmatched vertices in final layer of V,
        # and is also used as a flag value for pred[u] when u is in the first layer
        preds = {}
        unmatched = []
        pred = dict([(u,unmatched) for u in graph])
        for v in matching:
            del pred[matching[v]]
        layer = list(pred)
        
        # repeatedly extend layering structure by another pair of layers
        while layer and not unmatched:
            newLayer = {}
            for u in layer:
                for v in graph[u]:
                    if v not in preds:
                        newLayer.setdefault(v,[]).append(u)
            layer = []
            for v in newLayer:
                preds[v] = newLayer[v]
                if v in matching:
                    layer.append(matching[v])
                    pred[matching[v]] = v
                else:
                    unmatched.append(v)
        
        # did we finish layering without finding any alternating paths?
        if not unmatched:
            unlayered = {}
            for u in graph:
                for v in graph[u]:
                    if v not in preds:
                        unlayered[v] = None
            return (matching,list(pred),list(unlayered))

        # recursively search backward through layers to find alternating paths
        # recursion returns true if found path, false otherwise
        def recurse(v):
            if v in preds:
                L = preds[v]
                del preds[v]
                for u in L:
                    if u in pred:
                        pu = pred[u]
                        del pred[u]
                        if pu is unmatched or recurse(pu):
                            matching[v] = u
                            return 1
            return 0

        for v in unmatched: recurse(v)
## end of http://code.activestate.com/recipes/123641/ }}}

def solve():
    G = {}
    london = set()
    stockholm = set()
    m = int(sys.stdin.readline())
    for i in range(m):
        line = sys.stdin.readline()
        S,L = line.split()
        S,L = int(S),int(L)
        stockholm.add(S)
        london.add(L)
        if S in G:
            G[S].append(L)
        else:
            G[S] = [L]

    # http://en.wikipedia.org/wiki/K%C3%B6nig%27s_theorem_(graph_theory)
    M,A,B = bipartiteMatch(G)
    print M
    N = {}
    for s in G:
        for l in G[s]:
            if l in M and M[l] == s:
                continue
            if s in N:
                N[s].append(l)
            else:
                N[s] = [l]

    print N
        
    T = set()
    unchecked = stockholm - set(A)
    while unchecked:
        current = unchecked.pop()
        T.add(current)
        if current in M:
            unchecked.add(M[current])
        elif current in N:
            for l in N[current]:
                if l not in T:
                    unchecked.add(l)
    print T
    cover = ( stockholm - T ) | ( london & T )
    print len(cover)
    for k in cover:
        print k
    

if __name__ == "__main__":
    solve()
