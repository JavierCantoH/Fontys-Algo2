from os import PRIO_PGRP
from traceback import print_tb
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import networkx as nx
#import random
#from itertools import combinations, groupby

def generateGraph(numberOfNodes, probability, comesFromConnectSubgraphs):
    print(probability)
    n = int(numberOfNodes) # nodes
    e = ((int(probability) * (n-1)) / 100) * (n-1) # edges
    print("Number of edges = ")
    print(e)
    seed = 20160 # seed random number generators for reproducibility

    G = nx.gnm_random_graph(n, e, seed = seed) 
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
        #connectSubgraphs(generateGraph(numberOfNodes, probability, True))

window.close()