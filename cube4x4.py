import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import json

class Sticker:
    def __init__(self, on=False, color=None):
        self.on = on
        self.color = color
    def set_on(self):
        self.on = True
    def set_off(self):
        self.on = False

class Cube4x4:
    def __init__(self):
        # Define the face colors and create a 6 x 4 x 4 matrix contianing the information and position of each sticker
        # Each sticker has information about it's color and it's unfixed-in-face on state
        
        file_path = 'color_data.json'
        # Open the file and load the JSON data
        with open(file_path, 'r') as file:
            face_colors = json.load(file)
        #face_colors = {'A': '#13bc15', 'B': '#efefef', 'C': '#0000ff', 'D': '#ff0000', 'E': '#d5cd00', 'F': '#ff8a00'}
        faces = [np.full((4, 4), Sticker(on=True, color=face_colors[letter])) for letter in 'ABCDEF']
        faces_df_list = [pd.DataFrame(face) for face in faces]
        self.cube = pd.DataFrame([faces_df_list], columns=list(face_colors.keys()))

        # (for fixed-on-face mode) Create a fixed-on-face cube that holds the on state of every tile
        faces = [np.full((4, 4), True) for letter in 'ABCDEF']
        faces_df_list = [pd.DataFrame(face) for face in faces]
        self.tiles = pd.DataFrame([faces_df_list], columns=list(face_colors.keys()))

        # store every move used
        self.moves = []
    
    def move_F(self):
        self.moves.append("FRONT")
        last_row_B = self.get_face('B').iloc[3].tolist()
        first_col_D = self.get_face('D').iloc[:, 0].tolist()
        first_row_E = self.get_face('E').iloc[0].tolist()
        last_col_F = self.get_face('F').iloc[:, 3].tolist()
        
        # Rotate face A by 90 degrees clockwise
        self.cube['A'][0] = self.get_face('A').transpose().iloc[:, ::-1]
        # barrel shift columns and rows
        self.get_face('B').iloc[3] = last_col_F[::-1]
        self.get_face('D').iloc[:, 0] = last_row_B
        self.get_face('E').iloc[0] = first_col_D[::-1]
        self.get_face('F').iloc[:, 3] = first_row_E

    def move_f(self):
        self.moves.append("front")
        third_row_B = self.get_face('B').iloc[2].tolist()
        second_col_D = self.get_face('D').iloc[:, 1].tolist()
        second_row_E = self.get_face('E').iloc[1].tolist()
        third_col_F = self.get_face('F').iloc[:, 2].tolist()
        
        # barrel shift columns and rows
        self.get_face('B').iloc[2] = third_col_F[::-1]
        self.get_face('D').iloc[:, 1] = third_row_B
        self.get_face('E').iloc[1] = second_col_D[::-1]
        self.get_face('F').iloc[:, 2] = second_row_E

    def move_R(self):
        self.moves.append("RIGHT")
        last_col_A = self.get_face('A').iloc[:, 3].tolist()
        last_col_B = self.get_face('B').iloc[:, 3].tolist()
        last_col_E = self.get_face('E').iloc[:, 3].tolist()
        first_col_C = self.get_face('C').iloc[:, 0].tolist()
        self.cube['D'][0] = self.get_face('D').transpose().iloc[:, ::-1]
        self.get_face('A').iloc[:, 3] = last_col_E
        self.get_face('B').iloc[:, 3] = last_col_A
        self.get_face('E').iloc[:, 3] = first_col_C[::-1]
        self.get_face('C').iloc[:, 0] = last_col_B[::-1]
    
    def move_r(self):
        self.moves.append("right")
        third_col_A = self.get_face('A').iloc[:, 2].tolist()
        third_col_B = self.get_face('B').iloc[:, 2].tolist()
        third_col_E = self.get_face('E').iloc[:, 2].tolist()
        second_col_C = self.get_face('C').iloc[:, 1].tolist()
        self.get_face('A').iloc[:, 2] = third_col_E
        self.get_face('B').iloc[:, 2] = third_col_A
        self.get_face('E').iloc[:, 2] = second_col_C[::-1]
        self.get_face('C').iloc[:, 1] = third_col_B[::-1]

    def move_L(self):
        self.moves.append("LEFT")
        first_col_A = self.get_face('A').iloc[:, 0].tolist()
        first_col_B = self.get_face('B').iloc[:, 0].tolist()
        first_col_E = self.get_face('E').iloc[:, 0].tolist()
        last_col_C = self.get_face('C').iloc[:, 3].tolist()
        self.cube['F'][0] = self.get_face('F').transpose().iloc[:, ::-1]
        self.get_face('A').iloc[:, 0] = first_col_B
        self.get_face('B').iloc[:, 0] = last_col_C[::-1]
        self.get_face('E').iloc[:, 0] = first_col_A 
        self.get_face('C').iloc[:, 3] = first_col_E[::-1]

    def move_l(self):
        self.moves.append("left")
        second_col_A = self.get_face('A').iloc[:, 1].tolist()
        second_col_B = self.get_face('B').iloc[:, 1].tolist()
        second_col_E = self.get_face('E').iloc[:, 1].tolist()
        third_col_C = self.get_face('C').iloc[:, 2].tolist()
        self.get_face('A').iloc[:, 1] = second_col_B
        self.get_face('B').iloc[:, 1] = third_col_C[::-1]
        self.get_face('E').iloc[:, 1] = second_col_A 
        self.get_face('C').iloc[:, 2] = second_col_E[::-1]

    def move_U(self):
        self.moves.append("UP")
        first_row_A = self.get_face('A').iloc[0].tolist()
        first_row_F = self.get_face('F').iloc[0].tolist()
        first_row_D = self.get_face('D').iloc[0].tolist()
        first_row_C = self.get_face('C').iloc[0].tolist()
        self.cube['B'][0] = self.get_face('B').transpose().iloc[:, ::-1]
        self.get_face('A').iloc[0] = first_row_D
        self.get_face('F').iloc[0] = first_row_A
        self.get_face('D').iloc[0] = first_row_C[::-1]
        self.get_face('C').iloc[0] = first_row_F[::-1]

    def move_u(self):
        self.moves.append("up")
        second_row_A = self.get_face('A').iloc[1].tolist()
        second_row_F = self.get_face('F').iloc[1].tolist()
        second_row_D = self.get_face('D').iloc[1].tolist()
        second_row_C = self.get_face('C').iloc[1].tolist()
        self.get_face('A').iloc[1] = second_row_D
        self.get_face('F').iloc[1] = second_row_A
        self.get_face('D').iloc[1] = second_row_C[::-1]
        self.get_face('C').iloc[1] = second_row_F[::-1]


    # Returns a 4x4 DataFrame of a Face's Stickers
    def get_face(self, label):
        return self.cube[label][0]
    
    # Returns a 4x4 DataFrame of a Face's Sticker colors
    def get_face_colors(self, label):
        return self.get_face(label).applymap(lambda x: x.color)
    
    # Returns a 4x4 DataFrame of a Face's Sticker on state
    def get_face_on(self, label):
        return self.get_face(label).applymap(lambda x: x.on)

    # Returns a specific Sticker on a specific face
    def get_sticker(self, label, i, j):
        if isinstance(label, str):
            return self.cube[label].iloc[0].values[i][j]
        else:
            return self.cube[self.cube.iloc[:, label].name].iloc[0].values[i][j]
        
