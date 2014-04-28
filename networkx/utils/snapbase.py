import os
import subprocess
import tempfile
import networkx as nx
import sys


__author__="""Paul M"""

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

