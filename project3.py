from builtins import print
import networkx as nx
import numpy as np
import pandas as pd
import scipy as sp
import tqdm as tm
import json
import pickle
import matplotlib.pyplot as plt



def get_name():  # name function
    name = "Itay lorberboym"
    print(name)
    return name

def get_id():  # id function
    id = "314977596"
    print(id)
    return id

# ------------------------ 1 ---------------------- Centrality measures

# -- i --

def centrality_measures(network,node,iterations = 100):

    ans = {}
    degree_centrality_dict = nx.degree_centrality(network)
    ans['dc'] = degree_centrality_dict[node] #degree centrality
    closeness_centrality_dict = nx.closeness_centrality(network)
    ans['cs'] = closeness_centrality_dict[node] #closeness centrality
    betweenness_centrality_dict = nx.betweenness_centrality(network)
    ans['nbc'] = betweenness_centrality_dict[node] #betweenness cenrality
    pagerank_dict = nx.pagerank(network, max_iter=iterations)
    ans['pr'] = pagerank_dict[node] # page rank score
    authorities_dict = nx.hits(network,max_iter=iterations)[1]
    ans['auth'] = authorities_dict[node] #authority score

    return ans

# -- iii --

def single_steps_voucher(network):
    degree_centrality_dict = nx.degree_centrality(network)
    max_connections_node = max(degree_centrality_dict,key=degree_centrality_dict.get)
    return max_connections_node #node with highest degree centrality

# -- v --

def multiple_steps_voucher(network):
    closeness_dict = nx.closeness_centrality(network)
    lowest_num_of_steps_node = max(closeness_dict,key=closeness_dict.get)
    return lowest_num_of_steps_node #node with highest closeness centrality

# -- vii --

def multiple_steps_diminished_voucher(network):
    nodes = nx.nodes(network)
    nodes_values = {}
    for n in nodes: #check every node's score
        T = nx.bfs_tree(network, source=n, depth_limit=4)
        neighbors = list(nx.neighbors(T,n))
        nodes_values[n] = get_node_total_value(T,n,neighbors,0.025,1,4)
    most_valuabale_node = max(nodes_values, key=nodes_values.get)
    return most_valuabale_node

def get_node_total_value(network, node, neighbors,r, ticket_value, round):
    if ticket_value <= 0 or len(neighbors) == 0:
        return 0
    if round == 1: # when last round return the number of neighbors multiply by the ticket value
        return (ticket_value-r)*(len(neighbors))
    if len(neighbors) == 1: # when only one neighbor left procceed to the next round
        return (ticket_value-r) + get_node_total_value(network,neighbors[0],list(nx.neighbors(network, neighbors[0])),r,ticket_value-r,round-1)
    return (ticket_value-r) + get_node_total_value(network,node,neighbors[1:],r,ticket_value,round)\
           +get_node_total_value(network,neighbors[0],list(nx.neighbors(network, neighbors[0])),r,ticket_value-r,round-1)# go to next neighbor and procceed to next round

# -- ix --

def find_most_valuable(network):
    betweenness_dict = nx.betweenness_centrality(network)
    highest_betweenness_node = max(betweenness_dict, key=betweenness_dict.get)
    return highest_betweenness_node #node with highest betweenness centrality


# -- xi -- Bonus

def generic_multiple_steps_diminished_voucher(network,r,max_steps):
    ticket_first_value = 1
    r =r/100
    nodes = nx.nodes(network)
    nodes_values = {}
    for n in nodes:
        T = nx.bfs_tree(network, source=n, depth_limit=max_steps)
        neighbors = list(nx.neighbors(T, n))
        nodes_values[n] = get_node_total_value(T, n, neighbors, r, ticket_first_value, max_steps)
    most_valuabale_node = max(nodes_values,key=nodes_values.get)
    return most_valuabale_node








