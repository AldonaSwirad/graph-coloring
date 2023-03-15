import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

class Graph():
    def __init__(self):
        ''' Tworzy graf '''

        self.G = nx.Graph() # instancja glasy Graph z biblioteki nx
        self.is_colored = False 
        self.adjacency_list = {}
        self.node_colors = [] # lista przechowująca kolory wierzchołków grafu, kolejno dla każdego wierzchołka licząc od 0 
        
    def from_sudoku_board(self, sudoku_board, layout):
        ''' Tworzy graf na podstawie podanej planszy sudoku, sposób wyświetlania grafu zależy od parametru layout '''
        
        # sprawdzamy wielkość sudoku
        if sudoku_board.shape[0] == 9:
            n = 3
        else :
            n = 2
        
        # w zależności od wielkości sudoku tworzymy odpowiedni graf sudoku
        if n == 3:
            self.G = nx.sudoku_graph(n)
            for node, nodes_dict in self.G.adjacency():
                self.adjacency_list[node] = list(nodes_dict.keys())

        elif n == 2:
            self.G = nx.sudoku_graph(n)
            for node, nodes_dict in self.G.adjacency():
                self.adjacency_list[node] = list(nodes_dict.keys())

        # sposób wyświetlania grafu zależny od parametru layout
        if layout == 'grid':
            self.pos = dict(zip(list(self.G.nodes()), nx.grid_2d_graph(n * n, n * n)))
            
        elif layout == 'circular':
            self.pos = nx.circular_layout(self.G)

        # wstępnie koloruje graf na podstawie wartości w komórkach planszy sudoku
        self.map_colors_from_sudoku_board(sudoku_board=sudoku_board)

    def from_adjacency_list(self, adjacency_list):
        ''' Tworzy graf na podstawie podanej listy sąsiedztwa '''

        self.adjacency_list = adjacency_list
        self.node_colors = ['whitesmoke'] * len(adjacency_list) # tworzymy listę zależną od ilości wierzchołków, lista przechowuje domyślny kolor whitesmoke dla "niepokolorowanego" wierzchołka 
        self.G = nx.from_dict_of_lists(self.adjacency_list) 
        self.pos = nx.spring_layout(self.G) # odpowiada za rozłożenie wierzchołków

    def add_node(self, node):
        ''' Dodaje wierzchołek do listy sąsiedztwa '''
        
        # jeżeli wierzchołek nie znajduje się w liście sąsiedztwa
        if node not in self.adjacency_list.keys():
            self.adjacency_list[node] = [] # dodajemmy wierzchołek jako nowy klucz w słowniku, wartością jest pusta lista którą później wypełnimy sąsiadami danego wierzchołka

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

        color_list = ['whitesmoke', 'red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray'] # lista dostępnych kolorów wierzchołków 
        
        # przypisujemy wierzchołkowi kolor w zależności od wartości w planszy sudoku, dla wartości 0 kolorem oznaczającym "niepokolorowany" wierzchołek jest whitesmoke
        for row in sudoku_board:
            for node in row:
                self.node_colors.append(color_list[node])

    def standard_greedy_coloring(self):
        ''' Koloruje graf wykorzystując podstawową wersję algorytmu zachłannego '''

        adjacency_list = self.adjacency_list
        color_list = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'gold', 'beige', 'cyan'] # lista dostępnych kolorów wierzchołków, jest ich więcej ponieważ
                                                                                                                                # może okazać się że algorytm zachłanny nie bedzie w stanie 
                                                                                                                                # pokolorować grafu sudoku 9x9 9 kolorami

        # dla każdego wierzchołka w liście sąsiedztwa                                                                                           
        for node in range(len(adjacency_list)):
            if self.node_colors[node] != 'whitesmoke': # jeżeli wierzchołek ma już nadany kolor to pomiń aktualną iterację 
                continue

            used_colors = set() # zbiór przechowujący kolory sąsiadów danego wierzchołka, użyłem zbioru ponieważ ignoruje powtarzające się wartości

            # dla każego sąsiada w liście sąsiedztwa
            for neighbor in adjacency_list[node]:
                used_colors.add(self.node_colors[neighbor]) # do zbioru sąsiadujących kolorów dodaj kolor sąsiada

            # dla każdego dostępnego koloru z listy kolorów
            for color in color_list:
                if color not in used_colors: # jeżeli kolor nie jest wykorzystywany przez sąsiadów danego wierzchołka nadaj mu ten kolor
                    self.node_colors[node] = color
                    break
        
        self.is_colored = True # ustawia flagę odpowiedzialną za wyświetlanie liczby chromatycznej grafu
    
    def get_adjacency_matrix(self):
        ''' Zwraca macierz sąsiedztwa jako numpy array '''

        return nx.to_numpy_array(self.G)

    def get_node_degrees(self):
        ''' Zwraca stopnie wszystkich wierzchołków w grafie '''

        adjacency_matrix = self.get_adjacency_matrix()
        degrees = []
        
        for i in adjacency_matrix:
            degree = 0
            for j in i:
                degree += j

            degrees.append(degree)

        return degrees

    def display_graph_streamlit(self):
        ''' Wyświetla graf w streamlicie '''

        nx.draw_networkx(self.G, self.pos, with_labels=True, node_color = self.node_colors) # wyświetla graf
        st.pyplot(plt)
        
        # Jeżeli jest pokolorwany wyświetla również liczbę chromatyczną grafu
        if self.is_colored:
            st.write(f'Liczba chromatyczna grafu:  {len(set(self.node_colors))}')

    def display_graph_notebook(self):
        ''' Wyświetla graf w notebooku '''

        nx.draw(self.G, self.pos, with_labels=True, node_color = self.node_colors)
        plt.show()

        # Jeżeli jest pokolorwany wyświetla również liczbę chromatyczną grafu
        if self.is_colored:
            print(f'Liczba chromatyczna grafu:  {len(set(self.node_colors))}')

    def display_all_nodes(self):
        ''' Wypisuje w konsoli wszystkie wierzchołki '''

        print(self.adjacency_list.keys())

    def display_adjacency_list(self):
        '''Wypisuje w konsoli listę sąsiedztwa '''

        for node in self.adjacency_list.keys():
            print(f'{node} : {self.adjacency_list[node]}')

    def backtracking_coloring(self):
        ''' Koloruje graf 9 kolorami wykorzystując backtracking '''

        adjacency_list = self.adjacency_list
        num_nodes = len(adjacency_list)
        color_list = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray'] # lista kolorów, które mogą być przypisane do wierzchołków
        
        # sprawdza, czy można przypisać kolor do wierzchołka, zwraca true jeżeli żaden z sąsiadów wierzchołka nie ma przypisanego danego koloru
        def is_valid(node, color):
            for neighbor in adjacency_list[node]:
                if self.node_colors[neighbor] == color:
                    return False
            return True
        
        # rekurencyjnie próbuje przypisać kolory wszystkim wierzchołkom, jeżeli się to uda zwraca true
        def backtrack(node):
            if node == num_nodes:
                return True
            
            # jeżeli wierzchołek ma już przypisany kolor, to kolorujemy następny wierzchołek
            if self.node_colors[node] != 'whitesmoke':
                return backtrack(node + 1)
            
            # jeżeli nie ma przypisanego koloru próbujemy go przypisać z listy dostępnych kolorów
            for color in color_list:
                if is_valid(node, color):
                    self.node_colors[node] = color
                    
                    # jeżeli udało się przypisać kolor to kolorujemy następny wierzchołek
                    if backtrack(node + 1):
                        return True
                    
                    # jeżeli nie udało się przypisać koloru do następnych wierzchołków to cofamy się i próbujemy innych kolorów 
                    self.node_colors[node] = 'whitesmoke'
            
            # jeżeli nie udało się przypisać żadnego koloru do danego wierzchołka to zwracamy false
            return False
        
        # funkcja backtrack zaczyna od pierwszego tj. "zerowego" wierzchołka
        backtrack(0)
        self.is_colored = True # ustawia flagę odpowiedzialną za wyświetlanie liczby chromatycznej grafu

        



