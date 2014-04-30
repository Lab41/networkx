__author__ = 'aganesh'

import networkx as nx
import sys
import numpy as np
import matplotlib.pyplot as plt
import os

#Using undirected graph as model
#Assuming nodes are ints but can easily be extended




def test_separability(communities, G):

    #Demo sample metrics collected for visualization
    cond_list = []
    cut_list = []
    flake_list = []
    fomd_list = []
    tpr_list = []
    sep_list = []

    

    for c in communities:
        m = MetricCommunity(c, G)
        
        #Graph metrics against goodness metric of separability
        cond_list.append(m.conductance())
        cut_list.append(cut_ratio())
        flake_list.append(flake())
        fomd_list.append(fomd())
        tpr_list.append(tpr())
        sep_list.append(separability())

    #Sort the lists
    cond_list, cond_sep_list = (list(x) for x in zip(*sorted(zip(cond_list, sep_list), reverse=True)))
    cut_list, cut_sep_list = (list(x) for x in zip(*sorted(zip(cut_list, sep_list), reverse=True)))
    flake_list, flake_sep_list = (list(x) for x in zip(*sorted(zip(flake_list, sep_list), reverse=True)))
    fomd_list, fomd_sep_list = (list(x) for x in zip(*sorted(zip(fomd_list, sep_list), reverse=True)))
    tpr_list, tpr_sep_list = (list(x) for x in zip(*sorted(zip(tpr_list, sep_list), reverse=True)))

    #Rank numbering for graph
    x = np.linspace(1, len(sep_list), len(sep_list))

    #plot all the metrics against goodness
    plt.plot(x, cond_sep_list, label="conductance")
    plt.plot(x, cut_sep_list, label="cut ratio")
    plt.plot(x, flake_sep_list, label="flake ODF")
    plt.plot(x, fomd_sep_list, label="FOMD")
    plt.plot(x, tpr_sep_list, label="TPR")
    plt.legend(loc='best')

    #show the plot
    plt.xlabel("Rank")
    plt.ylabel("Separability")
    plt.show()

    
class GraphStats:

    def __init__(self, G):
        self.G = G
        self.graph_degree = G.degree(G.nodes_iter())
        self.median_degree = np.median(list(self.graph_degree.values()))
        self.num_nodes = len(G)


class MetricCommunity:
    '''
    Internal Connectivity Metrics
    '''

    def __init__(self, community, graph_stats):
        
        #dict nodes to internal degree
        self.internal_degree = community.degree()

        #dict nodes to internal and external degree
        self.degree = graph_stats.G.degree(community)

        #dict nodes to external degree
        self.external_degree = {key: self.degree[key] - self.internal_degree[key] for key in self.internal_degree.keys()}

        #Number of nodes,edges and boundary edges in community
        self.num_nodes_s = float(nx.number_of_nodes(community))
        self.num_edges_s = float(nx.number_of_edges(community))
        self.num_boundary_edges_s = float(sum(self.external_degree.values()))
        self.community = community
        
        self.graph_stats = graph_stats

    def simple_report(self):
        '''
        Prints metrics
        '''
        print "Density:             {}".format(self.density())
        print "Average Degree:      {}".format(self.avg_degree())
        print "Frac Over Med Deg:   {}".format(self.fomd())
        print "Tri Part Ratio:      {}".format(self.tpr())
        print "Expansion:           {}".format(self.expansion())
        print "Cut Ratio:           {}".format(self.cut_ratio())
        print "Conductance:         {}".format(self.conductance())
        print "Normalized Cut:      {}".format(self.normalized_cut())
        print "Out Degree Frac:     {}".format(self.odf())
        print "Max ODF:             {}".format(self.max_odf())
        print "Avg ODF:             {}".format(self.abg_odf())
        print "Separability:        {}".format(self.separability())


    def density(self):
        '''
        Calculates the internal edge density of the community
        
        Equation:  num_internal_edges / max_edges_possible
        '''
        return float(self.num_edges_s / ((self.num_nodes_s*(self.num_nodes_s - 1)) / 2))


    def avg_degree(self):
        '''
        Calculates the average internal degree of the nodes in the community
        '''
        return (2 * self.num_edges_s) / self.num_nodes_s


    def fomd(self):
        '''
        Fraction of nodes of S that have internal degree higher than the median degree value of entire set of graph nodes    
        '''
        node_greater_median = sum(1 for i in self.internal_degree.values() if i > self.graph_stats.median_degree)
        fomd = node_greater_median/self.num_nodes_s
        return fomd


    def tpr(self):
        '''
        Triangle Participation Ratio (TPR) is the fraction of nodes in S that belong to a triad
        Dictionary where nodes are the keys and values are the number of triangles that include the node as a vertex
        '''
        
        triangles = nx.triangles(self.community)

        tri_count = sum(x > 0 for x in triangles.values())
        tpr = tri_count / self.num_nodes_s
        return tpr

    def expansion(self):
        '''
        Measures the number of edges per node that point outside the cluster
        '''
        return self.num_boundary_edges_s/self.num_nodes_s


    def cut_ratio(self):
        '''     
        Fraction of existing edges leaving the cluster
        '''
        return self.num_boundary_edges_s / (self.num_nodes_s * (self.graph_stats.num_nodes - self.num_nodes_s))


    def conductance(self):
        '''
        Measures the fraction of total edge volume that points outside the cluster
        
        Equation: boundary_edges / num_directed_edges_originating_from_community
        '''

        return self.num_boundary_edges_s / ((2 * self.num_edges_s) + self.num_boundary_edges_s)


    def normalized_cut(self):
        '''
        Normalized Cut Metric
        '''

        return conductance_metric(self.num_edges_s, self.num_boundary_edges_s) + self.num_boundary_edges_s / ((2*(len(self.G.edges()) - self.num_edges_s)) + self.num_boundary_edges_s)



    def odf(self):
        '''
        Out Degree Fraction

        Calculates the out degree fraction (ODF) of each node in a community. The ODF is the fraction of edges from a node that that point outside the community

        returns ODF output 
        '''

        max_val = -1
        sum_val = 0.0
        few_count = 0.0

        for k, v in self.external_degree.items():
            div = float(v) / float(self.degree[k])
            sum_val += div
            if div > max_val:
                max_val = div
            if v > self.internal_degree[k]:
                few_count += 1

        flake_odf = few_count/ self.num_nodes_s
        max_odf = max_val
        avg_odf = sum_val / self.num_nodes_s

        return {"average":avg_odf, "flake":flake_odf, "max":max_odf}


    def separability():
        '''
        Measure ratio between the internal and the external number of edges of S
        '''
        return self.num_edges_s/self.num_boundary_edges_s





def main(argv):

    import networkx.utils.community_utils as cu 
    
    G = nx.gnm_random_graph(30,50) 
    graph_stats = GraphStats(G)
    nx.bigclam(G)

    communities = cu.read_communities("snap_cmtyvv.txt", G) 
    
    for c in communities:
        
        m = MetricCommunity(c, graph_stats)

        m.simple_report() 

    pass



    

if __name__ == "__main__":
    main(sys.argv[1:])
