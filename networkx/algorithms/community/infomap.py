import os
import subprocess
import tempfile
import networkx as nx
import networkx.utils.community_utils as cu
import sys


__author__="""Paul M"""

__all__ = ['infomap']



def main():
    
    G = nx.read_graphml('senate.graphml', node_type=int)
    #G = nx.gnm_random_graph(30,50)
    communities = infomap(G)

    print "Num Communities: {}".format(len(communities))

    for c in communities:
        print c.nodes()

def infomap(G, output="communities.txt"):
    '''
    InfoMap from Snap

    Parameters
    ------------
    G:              A NetworkX graph or edge list file
    output:         Communities output file (Default: communities.txt)

    '''

    return cu.divisive(G, '3', output)


if __name__ == "__main__":
    main()
