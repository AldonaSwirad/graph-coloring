import streamlit as st
import cv2
from PIL import Image
import numpy as np
from SudokuBoard import SudokuBoard
from Graph import Graph


uploaded_file = st.sidebar.file_uploader(label='Upload your sudoku board', type=["jpg","jpeg","png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_array = np.asarray(image)

    sudoku_board = SudokuBoard(image_array)
    sudoku_board.process_board_image()
    sudoku_board.split_board_image()

    board = sudoku_board.create_board()

    st.sidebar.image(image, caption='Uploaded sudoku')
    #st.sidebar.write(board)

g = Graph(type='sudoku4x4')
g.display_graph()
g.display_all_nodes()
g.display_adjacency_list()


    
