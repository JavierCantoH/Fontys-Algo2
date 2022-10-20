from os import PRIO_PGRP
from traceback import print_tb
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import networkx as nx
import random
from itertools import combinations, groupby

def connectSubgraphs(graph):
    components = dict(enumerate(nx.connected_components(graph)))
    components_combs = combinations(components.keys(), r=2)

    for _, node_edges in groupby(components_combs, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_comps = random.choice(node_edges)
        source = random.choice(list(components[random_comps[0]]))
        target = random.choice(list(components[random_comps[1]]))
        graph.add_edge(source, target)
    plt.figure(figsize=(12,6))
    nx.draw(graph, node_size=100, node_color='lightgreen')
    plt.show()

def generateGraph(numberOfNodes, probability, comesFromConnectSubgraphs):
    print(probability)
    n = int(numberOfNodes) # nodes
    e = ((int(probability) * (n-1)) / 100) * (n-1) # edges
    print("Number of edges = ")
    print(e)
    seed = 20160 # seed random number generators for reproducibility

    G = nx.gnm_random_graph(n, e, seed = seed) 
    if comesFromConnectSubgraphs:
        return G
    else:
        nx.draw(G, node_size= 100, node_color='lightblue')
        plt.show()


layout = [
        [sg.Text("Enter the number of nodes:")],    
        [sg.Input(key='-nodes-')],
        [sg.Text("Enter the probability (%) to generate the edges:")],    
        [sg.Input(key='-probability-')],
        [sg.Button("Generate Graph")],
        [sg.Button("Make it a connected graph")],
    ]

window = sg.Window("Algorithms Assignmet 1", layout)

while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED:
        break

    elif event == "Generate Graph":
        numberOfNodes = values['-nodes-']
        probability = values['-probability-']
        generateGraph(numberOfNodes, probability, False)
    
    # TODO: make this work without closing the window
    elif event == "Make it a connected graph":
        numberOfNodes = values['-nodes-']
        probability = values['-probability-']
        connectSubgraphs(generateGraph(numberOfNodes, probability, True))

window.close()