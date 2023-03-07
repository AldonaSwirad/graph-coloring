import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

class Graph():
    def __init__(self, adjacency_list=None, type=None):
        ''' Tworzy graf wykorzystując podaną listę sąsiedztwa, tworzy wybrany graf sudoku w zależnosci od parametru type '''

        # Tworzy pusty graf
        if adjacency_list == None and type == None:
            self.adjacency_list = {}
            self.G = nx.Graph()
        
        # Tworzy graf dużego sudoku
        elif adjacency_list == None and type == 'sudoku9x9':
            self.adjacency_list = {}
            self.G = nx.sudoku_graph(3)
            self.pos = dict(zip(list(self.G.nodes()), nx.grid_2d_graph(3 * 3, 3 * 3)))
            #self.pos = nx.circular_layout(self.G)
            for node, nodes_dict in self.G.adjacency():
                self.adjacency_list[node] = list(nodes_dict.keys())

        # Tworzy graf małego sudoku
        elif adjacency_list == None and type == 'sudoku4x4':
            self.adjacency_list = {}
            self.G = nx.sudoku_graph(2)
            self.pos = dict(zip(list(self.G.nodes()), nx.grid_2d_graph(2 * 2, 2 * 2)))
            #self.pos = nx.circular_layout(self.G)
            for node, nodes_dict in self.G.adjacency():
                self.adjacency_list[node] = list(nodes_dict.keys())
                
        else:
            # Tworzy graf wykorzystując podaną listę sąsiedztwa
            self.G = nx.Graph()
            self.adjacency_list = adjacency_list

    def add_node(self, node):
        ''' Dodaje wierzchołek do listy sąsiedztwa '''

        if node not in self.adjacency_list.keys():
            self.adjacency_list[node] = []

    def add_edge(self, edge):
        ''' Dodaje krawędź do listy sąsiedztwa '''

        edge = set(edge)
        node1, node2 = tuple(edge)
        for x, y in [(node1, node2), (node2, node1)]:
            if x in self.adjacency_list:
                self.adjacency_list[x].append(y)
            else:
                self.adjacency_list[x] = [y]

    def map_colors_from_sudoku_board(self, sudoku_board):
        ''' Wstępnie koloruje wierzchołki grafu na podstawie podanej planszy sudoku '''
        self.node_colors = []
        # Chujowo napisane ale jakoś działa 
        for row in sudoku_board:
            for node in row:
                if node == 0:
                    self.node_colors.append('whitesmoke')
                elif node == 1:
                    self.node_colors.append('red')
                elif node == 2:
                    self.node_colors.append('green')
                elif node == 3:
                    self.node_colors.append('blue')
                elif node == 4:
                    self.node_colors.append('yellow')
                elif node == 5:
                    self.node_colors.append('orange')
                elif node == 6:
                    self.node_colors.append('purple')
                elif node == 7:
                    self.node_colors.append('pink')
                elif node == 8:
                    self.node_colors.append('brown')
                elif node == 9:
                    self.node_colors.append('gray')

    def get_adjacency_matrix(self):
        ''' Zwraca macierz sąsiedztwa jako numpy array '''

        return nx.to_numpy_array(self.G)

    def display_graph_streamlit(self):
        ''' Wyświetla graf w streamlicie '''

        nx.draw_networkx(self.G, self.pos, with_labels=True, node_color = self.node_colors)
        st.pyplot(plt)

    def display_graph_notebook(self):
        ''' Wyświetla graf w notebooku, chyba bo nie testowałem'''

        nx.draw(self.G, self.pos, with_labels=True)
        plt.show()

    def display_all_nodes(self):
        ''' Wypisuje wszystkie wierzchołki '''

        print(self.adjacency_list.keys())

    def display_adjacency_list(self):
        '''Wypisuje listę sąsiedztwa '''

        for node in self.adjacency_list.keys():
            print(f'{node} : {self.adjacency_list[node]}')



