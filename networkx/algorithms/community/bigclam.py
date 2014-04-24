import os
import subprocess
import tempfile
import networkx as nx
import networkx.algorithms.snapbase as snap 
import sys


__author__="""Paul M"""

__all__ = ['bigclam']



#out of process
def serialize_graph(G):
    
    f = tempfile.mkstemp()
    filename = f[1]
    try:
        nx.write_edgelist(G, filename, delimiter='\t', data=False)
    except:
        return None

    return filename

    

def main():
    
    G = nx.gnm_random_graph(30,50)
    girvan_newman(G)
    #bigclam(G)



def setup(G):
    
    try:
        snap_home = os.environ[ENV_SNAPPATH_VAR] 
    except KeyError as e:
        print "Be sure to set your snap base path in the environment variable \"{}\"".format(ENV_SNAPPATH_VAR)
        return None,None,None

    filename = None
    is_temp_file = False

    if isinstance(G, basestring):
        if os.path.exists(G):
            filename = G
    else:
        filename  = serialize_graph(G)

    if filename is None:
        print "Unable to serialize the graph"

    return (snap_home, filename, is_temp_file)



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
    
    snap_home, graph_file, delete_file_after = setup(G)

    if graph_file is None:
        return

    path_bigclam = os.path.join(snap_home, "examples", "bigclam", "bigclam")

    try:

        out = subprocess.Popen([path_bigclam,"-o:"+data_prefix,"-i:"+graph_file,"-l:"+node_filepath,"-c:"+str(detect_comm), "-mc:"+str(min_comm), "xc:"+str(max_comm), "-nc:"+str(trials), "-nt:"+str(threads), "-sa:"+str(alpha), "-sb:"+str(beta)]).wait()
        
    except TypeError as e:
        print "Error occurred: {}".format(e)
        return     
  

    out.wait()

    if delete_file_after:
        os.remove(graph_file)




def girvan_newman(G, output="communities.txt"):
    '''
    Girvan-Newman from Snap

    Parameters
    ------------
    G:              A NetworkX graph or edge list file
    output:         Communities output file (Default: communities.txt)

    '''
    
    return base_edge_cut(G, 1, output)



def clauset_newman_moore(G, output="communities.txt"):
    '''
    Clauset-Newman-Moore from Snap

    Parameters
    ------------
    G:              A NetworkX graph or edge list file
    output:         Communities output file (Default: communities.txt)

    '''
    
    return base_edge_cut(G, 2, output)



def infomap(G, output="communities.txt"):
    '''
    InfoMap from Snap

    Parameters
    ------------
    G:              A NetworkX graph or edge list file
    output:         Communities output file (Default: communities.txt)

    '''
    
    return base_edge_cut(G, 3, output)



def base_edge_cut(G, algo_id, output):
    '''
    Girvan-Newman from Snap

    Parameters
    ------------
    G:              A NetworkX graph or edge list file
    output:         Communities output file (Default: communities.txt)

    '''
    
    snap_home, graph_file, delete_file_after = setup(G)

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
    



if __name__ == "__main__":
    main()
