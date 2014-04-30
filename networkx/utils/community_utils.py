import os
import subprocess
import tempfile
import networkx as nx
import sys


__author__="""Paul M"""

__all__ = []


def read_communities(f_name, G):
    
    comm_list = list()

    with open(f_name, 'rb') as community_file:
        for line in community_file:
            comm_list.append(G.subgraph(map(int, line.split())))

    return comm_list




def divisive(G, algo_id, output):

    snap_home, graph_file, delete_file_after = nx.algorithms.snapbase.setup(G)

    if graph_file is None:
        return

    path_girvan_newman = os.path.join(snap_home, "examples", "community", "community")


    try:
        out = subprocess.Popen([path_girvan_newman, "-i:"+graph_file, "-o:"+output, "-a:1"]) 
    except TypeError as e:
        print "Error occurred: {}".format(e)
        return
    
    out.wait()

    if delete_file_after:
        os.remove(graph_file)
    
