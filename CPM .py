# mathmodel23_v1.py
# Demo23 of mathematical modeling algorithm
# Demo of critical path method (CPM)  with NetworkX
# Copyright 2021 YouCans, XUPT
# Modified by Anpoe
# Crated：2021-07-26
# Modified: 2022-1-28


##################### import freamework ######################

import matplotlib.pyplot as plt  # import Matplotlib to plot graph
import networkx as nx  # import NetworkX to create directed graph
import csv # import to read csv file

#################### define function ####################

#################### Input and process csv file #######################
def CSV_read(Path):
    
    # Create 3 empty appends
    x = []
    y = []
    w = []

    # read csv file and add numbers to appends x, y, w
    with open(Path, 'r') as f:
        data=csv.reader(f, delimiter = ',')  
        for row in data:
            x.append(row[0])
            y.append(row[1])
            w.append(row[2])

    # calculate how many edges in x
    edge_no = len(x)
    # calculate the nodes number 
    node_no = int(max(x + y))

    # make DG useable out of function
    global DG
    # Create an empty directed graph
    DG = nx.DiGraph()  
    # Activity on edge network(AOE), nodes represent events or states, and directed edges represent activities
    DG.add_nodes_from(range(1, node_no), VE=0, VL=0)
    #use for loop to add weights from x,y,w appends (receive from csv file) muti times
    for i in range(0, edge_no):
        # Add multiple weight assigned edges to the graph: (node1:x,node2:y,weight:w)
        DG.add_weighted_edges_from([(int(x[i]),int(y[i]),int(w[i]))]) 

    # make lenNodes and topoSeq useable out of function
    global lenNodes
    global topoSeq
    lenNodes = len(DG.nodes)  # Number of nodes
    topoSeq = list(nx.topological_sort(DG))  # Topological Sequence

    return()

#################### Data Proces: Topology Calculation ####################
def Topo_cal(lenNodes, topoSeq):
    # --- Calculate the VE of each node: the earliest time of the event ---
    VE = [0 for i in range(lenNodes)]  # Initialization: the earliest time of the event
    for i in range(lenNodes):
        for e in DG.in_edges(topoSeq[i]):  # Iterate over the incoming edges of nodes topoSeq[i]
            VEij = DG.nodes[e[0]]["VE"] + DG[e[0]][e[1]]["weight"]  # Earliest time of the route
            if VEij > VE[i]: VE[i] = VEij  # If the route takes longer
        DG.add_node(topoSeq[i], VE=VE[i])  # Adding the earliest time of the node
    # --- Calculate the VL: event latest time for each node ---
    revSeq = list(reversed(topoSeq))  #  Reverses the topological sequence in order to calculate VL backwards from the endpoint
    VL = [DG.nodes[revSeq[0]]["VE"] for i in range(lenNodes)]  # Initialization: the latest time of the event is the maximum value of VE
    for i in range(lenNodes):
        for e in DG.out_edges(revSeq[i]):  # Iterate over the outgoing nodes of the vertex revSeq[i]
            VLij = DG.nodes[e[1]]["VL"] - DG[e[0]][e[1]]["weight"]  # The latest time of the route
            if VLij < VL[i]: VL[i] = VLij  # If the route takes longer
        DG.add_node(revSeq[i], VL=VL[i])  # Adding the latest time of the node
    print("\nEarliest time of the node (event): VE, Latest time VL:")
    for n in DG.nodes:  # Iterating over the vertices of a directed graph
        print("\tEvent {}:\tVE= {}\tVL= {}".format(n, DG.nodes[n]["VE"], DG.nodes[n]["VL"]))
    return()

####################### Data process: Minimum Time ##########################
def CPM_find():
    # --- Calculate ES, LS for each edge: earliest start time, latest start time for each work ---
    global cpDG
    cpDG = nx.DiGraph()  # Create a new empty directed graph to save the critical path
    print("\nEarliest time of the edge (work): ES, Latest time LS:")
    for e in DG.edges:  # Iterating over the edges of a directed graph
        DG[e[0]][e[1]]["ES"] = DG.nodes[e[0]]["VE"]  # Earliest start equals to earliest time of the event
        DG[e[0]][e[1]]["LS"] = DG.nodes[e[1]]["VL"] - DG[e[0]][e[1]]["weight"]  # The latest start time equals to the latest event time minus weight
        if DG[e[0]][e[1]]["ES"] == DG[e[0]][e[1]]["LS"]:  # if ES equals to LS, then the edge is a cricital path. 
            cpDG.add_edge(e[0], e[1], weight=DG[e[0]][e[1]]["weight"])  # Then adding the edge to cricital path
        print("\tWork {}:\tES= {}\tLS= {}\tDU= {}".format(e, DG[e[0]][e[1]]["ES"], DG[e[0]][e[1]]["LS"],
                                                        DG[e[0]][e[1]]["weight"]))
    # Calculate the shortest work time for the project and print the detials. 
    lenCP = sum(cpDG[e[0]][e[1]]["weight"] for e in cpDG.edges)
    print("\nCritical Path:{}".format(cpDG.edges))  
    print("Shortest Time To Complete:{}".format(lenCP))
    return(DG,cpDG.edges)

######################### Output: Plot ############################
def PLOT():
    # Plot directed network diagrams
    fig, ax = plt.subplots(figsize=(10, 6))
    pos = nx.kamada_kawai_layout(DG)  # Specify the nodes' position
    labels = nx.get_edge_attributes(DG, "weight")  #label the weight
    nx.draw_networkx_nodes(DG, pos, node_color='orange', node_size=400)  # Set the color and width of the specified node
    nx.draw_networkx_labels(DG, pos)  # Set the label of the specified node
    nx.draw_networkx_edges(DG, pos, edge_color='dimgrey', style='solid')  # Set the color and line type of the specified edge
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=labels, font_color='dimgrey')  # Set edge weights
    nx.draw_networkx_edges(DG, pos, edgelist=cpDG.edges, edge_color='r', width=2)  # Hlighting Critical Path
    ax.set_title("Project network graph by Yixin")
    ax.text(16, 0, "Yixin Liu Output", color='gainsboro')
    plt.axis('on')
    plt.show()  
    return()


################## Apply Function in Calculation ##################

CSV_read('CAT_8nodes1.csv')
Topo_cal(lenNodes,topoSeq)
CPM_find()
PLOT()    




