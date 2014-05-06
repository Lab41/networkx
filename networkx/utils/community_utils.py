import os
import subprocess
import tempfile
import networkx as nx
import sys


__author__="""Paul M"""

__all__ = []

            
def read_communities_by_community(f_name, G):
    '''
    Reads a community file in the format where each line represents a community where the line is a list of nodes separated by white space
    '''

    comm_list = list()

    with open(f_name, 'rb') as community_file:
        
        for line in community_file:
            
            if line.startswith('#'):
                continue
            try:
                comm_list.append(G.subgraph(map(int, line.split())))
            except ValueError as e:
                print "Node type is unclear for line: {}".format(line)
                return

    c_id = 0

    #add the communities id's as attributes to each node
    for c in comm_list:
        for n,d in c.nodes(data=True):
            
            if d.has_key('community') is False:
                d['community'] = list()

            d['community'].append(c_id)
        
        c_id+=1

    return comm_list


def read_communities_by_node(f_name, G):
    '''
    Reads a community file where each line is a node and the community to which it belongs.s
    '''

    #dict with keys as community_id and values are a list of nodes
    comm_dict = {}
    comm_list = list()

    with open(f_name, 'rb') as community_file:
        for line in community_file:
            if line.startswith('#'):
                continue
            node_id, community_id = line.split()
            node_id = int(node_id)
            community_id = int(community_id)

            if comm_dict.has_key(community_id) == False:
                comm_dict[community_id] = list()
         
            try:
                if G.node[node_id].has_key('community') is False:
                    G.node[node_id]['community'] = list()
            except KeyError:
                print "ERROR: Currently the NetworkX extension does not support str node_types"
                return list()

            G.node[node_id]['community'].append(community_id)
            comm_dict[community_id].append(node_id)

    for k, v in comm_dict.iteritems():
        comm_list.append(G.subgraph(v))

    return comm_list
    





def divisive(G, algo_id, output):

    snap_home, graph_file, delete_file_after = nx.utils.snapbase.setup(G)

    if graph_file is None:
        return

    path_girvan_newman = os.path.join(snap_home, "examples", "community", "community")


    try:
        out = subprocess.Popen([path_girvan_newman, "-i:"+graph_file, "-o:"+output, "-a:"+algo_id]) 
    except TypeError as e:
        print "Error occurred: {}".format(e)
        return
    
    out.wait()

    if delete_file_after:
        os.remove(graph_file)
   
    return nx.utils.community_utils.read_communities_by_node(output, G)






