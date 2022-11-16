from tkinter.tix import InputOnly
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import itertools
from time import sleep
from progress.spinner import MoonSpinner

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

    def removeEdge(self, v1, v2):
        global degree
        if self.adjMatrix[v1][v2] == 0:
            print("No edge between %d and %d" % (v1, v2))
            return
        elif v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
            return
        self.adjMatrix[v1][v2] = 0
        self.adjMatrix[v2][v1] = 0
        degree = degree - 1
    
    def pendantVertices(self):
        pendantVertices = []
        edgesInNodesList = []
        valid, edgesInNodesList = getEdgesPerNodeAndValidate(g.adjMatrix, edgesInNodesList)
        for index, edge in enumerate(edgesInNodesList):
            if edge == 1:
                pendantVertices.append(index)
        return pendantVertices
                
    # TODO: fix this function
    def removeVertex(self, x):
        global numberOfNodes
        printAdjMatrix(self)
        for index, node in enumerate(range(self.vertices)):
            if x == node:
                numberOfNodes = numberOfNodes - 1
                #self.vertices.remove(x)
                self.adjMatrix.pop(index)
                for i in self.adjMatrix:
                    i.pop(index1)
                printAdjMatrix(self)

def printAdjMatrix(graph):
        A = np.array(graph.adjMatrix)
        print(np.matrix(A))

def drawGraph(graph):
        A = np.array(graph.adjMatrix)
        G = nx.from_numpy_matrix(A)
        nx.draw(G, node_color='lightblue', with_labels = 1)

def bruteVertexCover(graph, k, vertex_cover):
    state = "starting"
    spinner = MoonSpinner('Loading ')

    while state != 'FINISHED':
        if graph.vertices == 0:
            return vertex_cover

        if k == 0:
            return None
        
        for node in range(1, graph.vertices + 1):
            # print('Checking subsets of size', str(node))
            # iterate over k sized subsets and check if each of those subsets is a vertex cover, the subsets are all posible combinations of k size
            for vertex_cover in itertools.combinations(range(graph.vertices), node):
                spinner.next()
                valid, numOfEdgesPerNode = getEdgesPerNodeAndValidate(graph.adjMatrix, set(vertex_cover))
                if valid:
                    state = 'FINISHED'
                    return (set(vertex_cover))
    state = 'FINISHED'
    return None

def vertex_cover_kernelization(graph, k):
    kernel, vertex_cover = _kernelize(graph, k)

    if kernel.vertices > k ** 2 + k or kernel.vertices > k ** 2:
        return None
    return bruteVertexCover(kernel, k - len(vertex_cover), vertex_cover)

# TODO: finish this function
def _kernelize(graph, k):
    kernel = graph
    vertex_cover = set()
    reductions_can_be_made = True
    
    A = np.array(graph.adjMatrix)
    G = nx.from_numpy_matrix(A)
    
    while reductions_can_be_made:
        reduction_made = False
        for node in range(kernel.vertices):
            degree = G.degree[node]
            if k > 0 and degree > k:
                reduction_made = True
                kernel.removeVertex(node)
                vertex_cover.add(node)
                k -= 1
            elif degree == 0:
                kernel.removeVertex(node)

        if not reduction_made:
            reductions_can_be_made = False

    return kernel, vertex_cover

# TODO: week 4 
# def enhancedBruteForce:

# TODO: week 5 
# recursive kernelization or smart search tree

def getEdgesPerNodeAndValidate(g, S): 
    isValid = True
    # we create a list of [[0, 0, ...]] (only 1 list inside the list size of the graph adjmatrix)
    numOfEdgesInNode = [0] * len(g)
    # iterate through the adjMatrix
    for i in range(0, len(g)):
        for j in range(i, len(g)): # we start on i because we will be counting the edges twice otherwise
            if g[i][j] == 1: # check if there is an edge between 2 nodes in position [i][j]
                if (i not in S) and (j not in S): 
                    isValid = False
                    numOfEdgesInNode[i] += 1  # example: from 0 we can go to 1
                    numOfEdgesInNode[j] += 1  # example: from 1 we can go to 0
    return isValid, numOfEdgesInNode

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
        [sg.Button("Kernelization Vertex Cover")],
        [sg.Text("", key='-vertexCoverLabel-')],
        [sg.Button("+ Pendants"), sg.Button("- Pendants")],
        [sg.Button("+ Tops"), sg.Button("- Tops")],
    ]

window = sg.Window("Algorithms Assignmet 1", layout)

numberOfNodes: int
probability: int
g: Graph

# TODO: add comments to the code
# TODO UI stuff: move progress bar to ui

while True:
    event, values = window.read(timeout=10)
    if event == "EXIT":
        break
    elif event == "Generate Graph":
        input1 = values['-nodes-']
        input2 = values['-probability-']
        if input1 and input2 == '':
            text = "Null string"
            window['-vertexCoverLabel-'].Update(text)
        else:
            try:
                numberOfNodes = int(input1)
                probability = int(input2)
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
                text = "No integer"
                window['-vertexCoverLabel-'].Update(text)

    elif event == "Brute Vertex Cover":
        input3 = values['-vertexcover-']
        if input3 == '':
            text = "Null string"
            window['-vertexCoverLabel-'].Update(text)
        elif int(input3) >= numberOfNodes:
            text = "The input is bigger than the total number of nodes"
            window['-vertexCoverLabel-'].Update(text)
        else:
            try:
                numOfVertexCover = int(input3)
                initial_vertex_cover = []
                #printAdjMatrix(g)
                possibleSolutions = bruteVertexCover(g, numOfVertexCover, initial_vertex_cover)
                if len(possibleSolutions) <= numOfVertexCover:
                    text = "Graph has vertex cover of size: " + str(numOfVertexCover)
                else:
                    text = "Graph doesn't have vertex cover of size: " + str(numOfVertexCover)
                window['-vertexCoverLabel-'].Update(text)
            except:
                text = "No integer"
                window['-vertexCoverLabel-'].Update(text)
                
    elif event == "Kernelization Vertex Cover":
        input3 = values['-vertexcover-']
        if input3 == '':
            text = "Null string"
            window['-vertexCoverLabel-'].Update(text)
        elif int(input3) >= numberOfNodes:
            text = "The input is bigger than the total number of nodes"
            window['-vertexCoverLabel-'].Update(text)
        else:
            try:
                # TODO: finding isolated vertices, finding pendant vertices (and their adjacent vertices), finding tops verticeThose should be indicated in the graph picture with proper coloring of the vertices and/or edges.
                numOfVertexCover = int(input3)
                #printAdjMatrix(g)
                possibleSolutions = vertex_cover_kernelization(g, int(input3))
                if len(possibleSolutions) <= numOfVertexCover:
                    text = "Graph has vertex cover of size: " + str(numOfVertexCover)
                else:
                    text = "Graph doesn't have vertex cover of size: " + str(numOfVertexCover)
                window['-vertexCoverLabel-'].Update(text)
            except:
                text = "No integer"
                window['-vertexCoverLabel-'].Update(text)
    elif event == "- Pendants":
        # selects an arbitrary non-pendant vertex and makes it a pendant by removing arbitrary edges
        A = np.array(g.adjMatrix)
        G = nx.from_numpy_matrix(A)
        printAdjMatrix(g)
        pendantVerticesList = g.pendantVertices()
    
        randomNodeToDeleteEdges = random.choice(range(g.vertices))
        
        while randomNodeToDeleteEdges in pendantVerticesList:
            randomNodeToDeleteEdges = random.choice(range(g.vertices))
            
        global degree 
        degree = G.degree[randomNodeToDeleteEdges]
            
        while degree != 1 and degree > 0:
                    randomNode = random.choice(range(g.vertices))
                    g.removeEdge(randomNodeToDeleteEdges, randomNode)
        # TODO: draw the new graph
        printAdjMatrix(g)
    elif event == "+ Pendants":
        # selects an arbitrary pendant vertex and makes it non pendant by adding arbitrary edge
        printAdjMatrix(g)
        pendantVerticesList = g.pendantVertices()
        randomNode = random.choice(range(g.vertices))
        randomNodeToAddEdge = random.choice(pendantVerticesList)
        while randomNodeToAddEdge == randomNode:
           randomNodeToAddEdge = random.choice(pendantVerticesList) 
        g.addSingleEdge(randomNodeToAddEdge, randomNode)
        # TODO: draw the new graph
        printAdjMatrix(g)
    elif event == "- Tops":
        # TODO ask teacher what does should it do
        print()
    elif event == "+ Tops":
        # TODO ask teacher what does should it do
        print()
        