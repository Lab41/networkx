import os
import subprocess
import tempfile
import networkx as nx
import sys


__author__="""Paul M"""

__all__ = ['clauset_newman_moore']



def main():
    
    G = nx.gnm_random_graph(30,50)
    girvan_newman(G)
    #bigclam(G)




def clauset_newman_moore(G, output="communities.txt"):
    '''
    Clauset-Newman-Moore from Snap

    Parameters
    ------------
    G:              A NetworkX graph or edge list file
    output:         Communities output file (Default: communities.txt)

    '''
    
    return nx.algorithms.community.divisive.do_divisive(G, 2, output)



if __name__ == "__main__":
    main()
