import os
import subprocess
import tempfile
import networkx as nx
import networkx.utils.community_utils as cu  
import sys


__author__="""Paul M"""

__all__ = ['girvan_newman']


def main():
    
    #G = nx.gnm_random_graph(30,50)
    G = nx.read_graphml('senate.graphml', node_type=int) 
    comm_list = girvan_newman(G)

    for c in comm_list:
        print c.nodes()



def girvan_newman(G, output="communities.txt"):
    '''
    Girvan-Newman from Snap

    Parameters
    ------------
    G:              A NetworkX graph or edge list file
    output:         Communities output file (Default: communities.txt)

    '''
    
    return cu.divisive(G,"1",output)

if __name__ == "__main__":
    main()
