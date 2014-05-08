__author__ = 'aganesh, paulm'

import networkx as nx
import sys
import numpy as np
import matplotlib.pyplot as plt
import os

def f1(communities, ground_truth, out):

    out.write("Evaluating F1 score\n")
    out.write("{} Communities in ground truth\n".format(len(ground_truth)))
    out.write("{} Communities in results\n".format(len(communities)))

    f1_sum_0 = sum([get_highest_f1(x, communities) for x in ground_truth])
    f1_sum_1 = sum([get_highest_f1(x, ground_truth) for x in communities])
    
    final_score = .5 * (  1.0/float(len(ground_truth)) * f1_sum_0 + 1.0/float(len(communities)) * f1_sum_1)
    
    print out.write("F1 Score: {}\n".format(final_score))
    



def get_highest_f1(src_community, community_list):
    """
    Find the best matching community in the list using f1, then return highest score 

    :param src_community:   community to base search on
    :param community_list:  list of communities to search in 
    """
    
    max_f1 = 0.0

    for matchee in community_list:
        score = f1_score(src_community, matchee)
        if score > max_f1:
            max_f1 = score
    
    return max_f1



def f1_score(community_a, community_b):
    """
    according to http://en.wikipedia.org/wiki/F1_score
    
    F_1 = 2 * (precision * recall) / (precision + recall)
    
    where precision = #matched / len (set_a)
          recall = #matched / len(set_b)
    """

    intersect_set = set(community_a).intersection(community_b)
    overlap_len = len(intersect_set)
   
    if overlap_len > 0:
        precision = float(overlap_len) / float(len(community_a))
        recall = float(overlap_len) / float(len(community_b))
        return 2.0 * (precision * recall) /  (precision + recall)
    else:
        return 0.0





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
        self.num_edges = len(G.edges())

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

    def do_report(self, f):
        '''
        Prints metrics
        '''

        report =  """
            nodes; {nodes}
            Density:             {density}
            Average Degree:      {avg_degree}
            Frac Over Med Deg:   {fomd}
            Tri Part Ratio:      {tpr}
            Expansion:           {expansion}
            Cut Ratio:           {cut_ratio}
            Conductance:         {conductance}
            Normalized Cut:      {normalized_cut}
            Out Degree Frac:     {odf}
            Separability:        {separability}
        """.format( nodes=self.community.nodes(), 
                    density=self.density(), 
                    avg_degree=self.avg_degree(), 
                    fomd=self.fomd(), 
                    tpr=self.tpr(),  
                    expansion=self.expansion(),
                    cut_ratio=self.cut_ratio(),
                    conductance=self.conductance(),
                    normalized_cut=self.normalized_cut(),
                    odf=self.odf(),
                    separability=self.separability())

        f.write(report)

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

        return self.conductance() + self.num_boundary_edges_s / ((2* self.graph_stats.num_edges - self.num_edges_s) + self.num_boundary_edges_s)



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


    def separability(self):
        '''
        Measure ratio between the internal and the external number of edges of S
        '''
        return self.num_edges_s/self.num_boundary_edges_s



def show_report(comm_metrics, f):
   
    f.write("===== Metrics Description =====\n\n")
    f.write("Density\n")
    f.write(MetricCommunity.density.__doc__)
    f.write("\n")
    f.write("Average Degree\n")
    f.write(MetricCommunity.avg_degree.__doc__)
    f.write("\n")
    f.write("Fraction Over Median Degree (FOMD)")
    f.write(MetricCommunity.fomd.__doc__)
    f.write("\n")
    f.write("Triangle Participation Ratio (TRP)")
    f.write(MetricCommunity.tpr.__doc__)
    f.write("\n")
    f.write("Expansion")
    f.write(MetricCommunity.expansion.__doc__)  
    f.write("\n")
    f.write("Cut-Ratio")
    f.write(MetricCommunity.cut_ratio.__doc__)
    f.write("\n")
    f.write("Conductance")
    f.write(MetricCommunity.conductance.__doc__)
    f.write("\n")
    f.write("Normalized Cut")
    f.write(MetricCommunity.normalized_cut.__doc__)
    f.write("\n")
    f.write("Out Degree Fraction (odf)")
    f.write(MetricCommunity.odf.__doc__)
    f.write("\n")
    f.write("Separability")
    f.write(MetricCommunity.separability.__doc__)
    f.write("\n")
    f.write("\n\n")
    f.write("===== Community Metrics =====")
    for m in comm_metrics:
        pass
        m.do_report(f)

    f.write("\n\n")

def ground_truth_metrics(comms, ground_truth, G, out):
   f1(comms, ground_truth, out) 




def run_analysis(communities, G, ground_truth=None, report_file=None):
    '''
    Performs analysis on communities and optionally ground truth

    '''
    
    print "Running metrics analysis"

    if report_file:
        out = open(report_file, 'w')
    else: 
        out = sys.stdout


    comm_metrics = list()
    graph_stats = GraphStats(G)

    for c in communities:
        comm_metrics.append(MetricCommunity(c, graph_stats))
            
    show_report(comm_metrics, out)
    
    if ground_truth:
        f1(communities, ground_truth, out)    

def main(argv):

    import networkx.utils.community_utils as cu 
    
    G = nx.gnm_random_graph(30,50) 
    nx.write_edgelist(G, "g.edgelist", delimiter="\t", data=False)
    communities = nx.bigclam(G)
    run_analysis(communities, G)
    

if __name__ == "__main__":
    main(sys.argv[1:])
