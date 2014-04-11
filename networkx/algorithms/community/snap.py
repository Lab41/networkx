#import snap
import os
import subprocess
import tempfile
import networkx as nx

__author__="""tbd"""

__all__ = ['bigclam']


ENV_SNAPPATH_VAR = "SNAPHOME"


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
    run_bigclam(G)



def setup():
    
    try:
        snap_home = os.environ[ENV_SNAPPATH_VAR] 
    except KeyError as e:
        print "Be sure to set your snap base path in the environment variable \"{}\"".format(ENV_SNAPPATH_VAR)
        return None

    return snap_home

def bigclam(G, data_prefix='dude', node_filepath='', detect_comm=100, min_comm=5, max_comm=100, trials=10, threads=4, alpha=0.05, beta=0.3):
    '''
    BigClam by Jure Leskovec

    Parameters
    ----------
    G : NetworkX graph

    ...

    ...
     
    '''
    snap_home = setup()

    if snap_home is None:
        return

    filename  = serialize_graph(G)
    
    if filename is None:
        print "Error serializing graph"
        return

    print "File: {}".format(filename)

    path_bigclam = os.path.join(snap_home, "examples", "bigclam", "bigclam")

    try:

        out = subprocess.Popen([path_bigclam,"-i:"+filename,"-l:"+node_filepath,"-c:"+str(detect_comm), "-mc:"+str(min_comm), "xc:"+str(max_comm), "-nc:"+str(trials), "-nt:"+str(threads), "-sa:"+str(alpha), "-sb:"+str(beta)]).wait()
        
    except TypeError as e:
        print "Error occurred: {}".format(e)
        return     
   

    print out
    os.remove(filename)


def snap_girvan_newman(G_nx):
    
    #first we need to convert the graph
    G_snap = switch_to_snap(G_nx)

    CmtyV = snap.TCnComV()
    modularity = snap.CommunityGirvanNewman(G_snap, CmtyV)
    for Cmty in CmtyV:
        print "Community: "
        for NI in Cmty:
            print NI

    print "The modularity of the network is %f" % modularity



if __name__ == "__main__":
    main()
