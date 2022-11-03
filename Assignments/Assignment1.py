from tkinter.tix import InputOnly
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

class Graph(object):
    def __init__(self, vertices):
        self.adjMatrix = []
        for i in range(vertices):
            self.adjMatrix.append([0 for i in range(vertices)])
        self.vertices = vertices

    def addSingleEdge(self, v1, v2):
        if v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
        else:
            self.adjMatrix[v1][v2] = 1
            self.adjMatrix[v2][v1] = 1
    
    def addEdges(self, probability):
        for node in range(self.vertices):
                if probability == 100:
                    for otherNode in range(self.vertices):
                        self.addSingleEdge(node, otherNode)
                elif getProbability(probability) == True:
                    randomNode = random.choice(range(self.vertices))
                    self.addSingleEdge(node, randomNode)
    

def printAdjMatrix(graph):
        A = np.array(graph.adjMatrix)
        print(np.matrix(A))

def drawGraph(graph):
        A = np.array(graph.adjMatrix)
        G = nx.from_numpy_matrix(A)
        nx.draw(G, node_color='lightblue')
    
def isNodeVertexCoverTrue(graph, start, num):
        count = 0
        visited = [False] * graph.vertices
        DFS(graph, start, visited)
        for nodeIndex, nodeValue in enumerate(visited):
            if (nodeValue == True):
                if nodeIndex == start:
                    print("same node")
                else:
                    count = count + 1
        if (num <= count):
            return True
        else:
            return False

def bruteVertexCover(graph, num):
    for node in range(graph.vertices):
        currentNode = isNodeVertexCoverTrue(graph, node, num)
        if currentNode == True:
            return ("Graph has at least one vertex cover of size: " + str(num))
        else:
            print("The current node doesn't have vertex cover")
    return ("Graph doesn't have vertex cover of size: " + str(num))


def getProbability(probability):
        p = float(probability / 100)
        return random.random() < p

def DFS(graph, start, visited):
    visited[start] = True
    for node in range(graph.vertices):
        if (graph.adjMatrix[start][node] == 1 and (not visited[node])):
            DFS(graph, node, visited)

def isGraphConnected(graph, start):
    count = 0
    visited = [False] * graph.vertices
    DFS(graph, start, visited)
    for b in visited:
        if (b == True):
            count = count + 1
    if (graph.vertices == count):
        return True
    else:
        return False

def makeItConnected(graph):
    for node in range(graph.vertices):
        nodeConnected = isGraphConnected(graph, node)
        if nodeConnected == True:
            print("Node is connected to the rest of the graph")
        else:
            graph.addSingleEdge(node, random.choice(range(graph.vertices)))
            makeItConnected(graph)


layout = [
        [sg.Button("EXIT")],
        [sg.Text("Enter the number of nodes:")],    
        [sg.Input(key='-nodes-')],
        [sg.Text("Enter the probability (%) to generate the edges:")],    
        [sg.Input(key='-probability-')],
        [sg.Button("Generate Graph")],
        [sg.Text("Enter the size for vertex cover (should be less tha the number of vertices):")],    
        [sg.Input(key='-vertexcover-')],
        [sg.Button("Brute Vertex Cover")],
        [sg.Text("", key='-vertexCoverLabel-')],
    ]

window = sg.Window("Algorithms Assignmet 1", layout)

numberOfNodes: int
probability: int
g: Graph

# TODO: button to restart textfields insted of closing and reopening every single time
# TODO: add comments to the code

# TODO: fix connected graph
# TODO: complelty change brute vertex cover
# TODO: week 3

while True:
    event, values = window.read(timeout=10)
    if event == "EXIT":
        break
    elif event == "Generate Graph":
        input1 = values['-nodes-']
        input2 = values['-probability-']
        if input1 and input2 == '':
            print('Null string')
        else:
            try:
                numberOfNodes = int(input1)
                probability = int(input2)
                print(f'Integer: {numberOfNodes}')
                print(f'Integer: {probability}')
                g = Graph(numberOfNodes)
                g.addEdges(probability)
                printAdjMatrix(g)
                plt.figure(1)
                drawGraph(g)
                makeItConnected(g)
                printAdjMatrix(g)
                plt.figure(2)
                drawGraph(g)
                plt.show(block = False)
            except:
                print("Not Integer")

    elif event == "Brute Vertex Cover":
        input3 = values['-vertexcover-']
        if input3 == '':
            print('Null string')
        else:
            try:
                numOfVertexCover = int(input3)
                print(f'Integer: {numOfVertexCover}')
                printAdjMatrix(g)
                text = bruteVertexCover(g, numOfVertexCover)
                window['-vertexCoverLabel-'].Update(text)
            except:
                print("Not Integer")
#window.close()