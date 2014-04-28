import os
import subprocess
import tempfile
import networkx as nx
import networkx.utils.snapbase as snap 
import sys


__author__="""Paul M"""

__all__ = ['bigclam']


def main():
    
    G = nx.gnm_random_graph(30,50)
    bigclam(G)



def bigclam(G, data_prefix='snap_', node_filepath='', detect_comm=100, min_comm=5, max_comm=100, trials=10, threads=4, alpha=0.05, beta=0.3):
    '''
    BigClam from Snap

    Parameters
    ----------
    G :                 A NetworkX graph or edge list file
    node_file_path:     Input file name for node names (Node ID, Node label)  
    detect_comm:        The number of communities to detect (-1: detect automatically) (Default: 100)
    min_comm:           Minimum number of communities to try (Default = 5)
    max_comm:           Maximum number of communities to try (Default = 100)
    trials:             How many trials for the number of communities (Default = 10)
    threads:            Number of threads for parallelization (Default = 4)
    alpha:              Alpha for backtracking line search (Default = 0.05)
    beta:               Beta for backtracking line search (Default = 0.3)

     
    '''
    
    snap_home, graph_file, delete_file_after = snap.setup(G)

    if graph_file is None:
        return

    path_bigclam = os.path.join(snap_home, "examples", "bigclam", "bigclam")

    try:

        out = subprocess.Popen([path_bigclam,"-o:"+data_prefix,"-i:"+graph_file,"-l:"+node_filepath,"-c:"+str(detect_comm), "-mc:"+str(min_comm), "xc:"+str(max_comm), "-nc:"+str(trials), "-nt:"+str(threads), "-sa:"+str(alpha), "-sb:"+str(beta)]).wait()
        
    except TypeError as e:
        print "Error occurred: {}".format(e)
        return     
  

    if delete_file_after:
        os.remove(graph_file)



if __name__ == "__main__":
    main()
