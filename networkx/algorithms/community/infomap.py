import os
import subprocess
import tempfile
import networkx as nx
import sys


__author__="""Paul M"""

__all__ = ['infomap']



def main():
    
    G = nx.gnm_random_graph(30,50)
    infomap(G)


def infomap(G, output="communities.txt"):
    '''
    InfoMap from Snap

    Parameters
    ------------
    G:              A NetworkX graph or edge list file
    output:         Communities output file (Default: communities.txt)

    '''

    print dir(nx.algorithms.community)

    return nx.algorithms.community.divisive_base.do_divisive(G, 3, output)



if __name__ == "__main__":
    main()
