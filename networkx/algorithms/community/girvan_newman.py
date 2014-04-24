import os
import subprocess
import tempfile
import networkx as nx
import sys


__author__="""Paul M"""

__all__ = ['girvan_newman']


def main():
    
    G = nx.gnm_random_graph(30,50)
    girvan_newman(G)
    #bigclam(G)



def girvan_newman(G, output="communities.txt"):
    '''
    Girvan-Newman from Snap

    Parameters
    ------------
    G:              A NetworkX graph or edge list file
    output:         Communities output file (Default: communities.txt)

    '''
    
    return nx.algorithms.community.divisive.do_divisive(G, 1, output)



if __name__ == "__main__":
    main()
