import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
from cube4x4 import *
from PyQt5.QtGui import QColor
import threading
import time
from synthesizer import *

class SequencerGUI(QMainWindow):
    def __init__(self):
        super(SequencerGUI, self).__init__()

        uic.loadUi("/home/user/Desktop/Music/Cube Sequencer/v5/sequencer_layout.ui", self)
        self.show()
        # 3D list of all labels
        self.L_A = [[self.L_A_00, self.L_A_01, self.L_A_02, self.L_A_03], 
                  [self.L_A_10, self.L_A_11, self.L_A_12, self.L_A_13], 
                  [self.L_A_20, self.L_A_21, self.L_A_22, self.L_A_23], 
                  [self.L_A_30, self.L_A_31, self.L_A_32, self.L_A_33]]
        self.L_B = [[self.L_B_00, self.L_B_01, self.L_B_02, self.L_B_03], 
                  [self.L_B_10, self.L_B_11, self.L_B_12, self.L_B_13], 
                  [self.L_B_20, self.L_B_21, self.L_B_22, self.L_B_23], 
                  [self.L_B_30, self.L_B_31, self.L_B_32, self.L_B_33]]
        self.L_C = [[self.L_C_00, self.L_C_01, self.L_C_02, self.L_C_03], 
                  [self.L_C_10, self.L_C_11, self.L_C_12, self.L_C_13], 
                  [self.L_C_20, self.L_C_21, self.L_C_22, self.L_C_23], 
                  [self.L_C_30, self.L_C_31, self.L_C_32, self.L_C_33]]
        self.L_D = [[self.L_D_00, self.L_D_01, self.L_D_02, self.L_D_03], 
                  [self.L_D_10, self.L_D_11, self.L_D_12, self.L_D_13], 
                  [self.L_D_20, self.L_D_21, self.L_D_22, self.L_D_23], 
                  [self.L_D_30, self.L_D_31, self.L_D_32, self.L_D_33]]
        self.L_E = [[self.L_E_00, self.L_E_01, self.L_E_02, self.L_E_03], 
                  [self.L_E_10, self.L_E_11, self.L_E_12, self.L_E_13], 
                  [self.L_E_20, self.L_E_21, self.L_E_22, self.L_E_23], 
                  [self.L_E_30, self.L_E_31, self.L_E_32, self.L_E_33]]
        self.L_F = [[self.L_F_00, self.L_F_01, self.L_F_02, self.L_F_03], 
                  [self.L_F_10, self.L_F_11, self.L_F_12, self.L_F_13], 
                  [self.L_F_20, self.L_F_21, self.L_F_22, self.L_F_23], 
                  [self.L_F_30, self.L_F_31, self.L_F_32, self.L_F_33]]
        self.label_gui_cube = [self.L_A, self.L_B, self.L_C, self.L_D, self.L_E, self.L_F]

        # 3D list of all buttons
        self.A = [[self.A_00, self.A_01, self.A_02, self.A_03], 
                  [self.A_10, self.A_11, self.A_12, self.A_13], 
                  [self.A_20, self.A_21, self.A_22, self.A_23], 
                  [self.A_30, self.A_31, self.A_32, self.A_33]]
        self.B = [[self.B_00, self.B_01, self.B_02, self.B_03], 
                  [self.B_10, self.B_11, self.B_12, self.B_13], 
                  [self.B_20, self.B_21, self.B_22, self.B_23], 
                  [self.B_30, self.B_31, self.B_32, self.B_33]]
        self.C = [[self.C_00, self.C_01, self.C_02, self.C_03], 
                  [self.C_10, self.C_11, self.C_12, self.C_13], 
                  [self.C_20, self.C_21, self.C_22, self.C_23], 
                  [self.C_30, self.C_31, self.C_32, self.C_33]]
        self.D = [[self.D_00, self.D_01, self.D_02, self.D_03], 
                  [self.D_10, self.D_11, self.D_12, self.D_13], 
                  [self.D_20, self.D_21, self.D_22, self.D_23], 
                  [self.D_30, self.D_31, self.D_32, self.D_33]]
        self.E = [[self.E_00, self.E_01, self.E_02, self.E_03], 
                  [self.E_10, self.E_11, self.E_12, self.E_13], 
                  [self.E_20, self.E_21, self.E_22, self.E_23], 
                  [self.E_30, self.E_31, self.E_32, self.E_33]]
        self.F = [[self.F_00, self.F_01, self.F_02, self.F_03], 
                  [self.F_10, self.F_11, self.F_12, self.F_13], 
                  [self.F_20, self.F_21, self.F_22, self.F_23], 
                  [self.F_30, self.F_31, self.F_32, self.F_33]]
                  
        self.gui_cube = [self.A, self.B, self.C, self.D, self.E, self.F]
        for i, face in enumerate(self.gui_cube):
            for j, row in enumerate(face):
                for k, elem in enumerate(row):
                    elem.clicked.connect(self.left_click_tial)
                    elem.setContextMenuPolicy(Qt.CustomContextMenu)
                    elem.customContextMenuRequested.connect(self.right_click_tial)

        self.tile_off_color = '#5b5b5b'
        self.toggled_color = '#fb00ff'
        self.untoggled_color = '#9A9996'
        self.my_cube = Cube4x4()
        self.tile_on = np.full((6, 4, 4), True, dtype=bool)
        self.face_num = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5}
        # Moves
        self.FRONT_MOVE.clicked.connect(lambda: self.move_cube('FRONT'))
        self.RIGHT_MOVE.clicked.connect(lambda: self.move_cube('RIGHT'))
        self.right_MOVE.clicked.connect(lambda: self.move_cube('right'))
        self.LEFT_MOVE.clicked.connect(lambda: self.move_cube('LEFT'))
        self.left_MOVE.clicked.connect(lambda: self.move_cube('left'))
        self.UP_MOVE.clicked.connect(lambda: self.move_cube('UP'))
        self.up_MOVE.clicked.connect(lambda: self.move_cube('up'))
        self.front_MOVE.clicked.connect(lambda: self.move_cube('front'))
        
        # Choosing tials
        self.sequence_indices = []
        self.choosing = False
        self.choose.clicked.connect(self.choose_sequence)

        self.stopping = False
        self.stop.clicked.connect(self.stop_sequence)
        # Run Sequence
        self.run.clicked.connect(self.startRunThread)

        # Tempo dial (use the value of the tempo dial to change clock)
        self.tempo_dial.valueChanged.connect(self.tempo_lcd.display)
        self.tempo_dial.setValue(120)
        self.tempo_dial.setRange(0, 500)

        self.green_dial.valueChanged.connect(self.green_lcd.display)
        self.green_dial.setValue(100)
        self.green_dial.setRange(0, 1000)

        self.white_dial.valueChanged.connect(self.white_lcd.display)
        self.white_dial.setValue(119)
        self.white_dial.setRange(0, 1000)

        self.blue_dial.valueChanged.connect(self.blue_lcd.display)
        self.blue_dial.setValue(133)
        self.blue_dial.setRange(0, 1000)

        self.red_dial.valueChanged.connect(self.red_lcd.display)
        self.red_dial.setValue(150)
        self.red_dial.setRange(0, 1000)

        self.yellow_dial.valueChanged.connect(self.yellow_lcd.display)
        self.yellow_dial.setValue(178)
        self.yellow_dial.setRange(0, 1000)

        self.orange_dial.valueChanged.connect(self.orange_lcd.display)
        self.orange_dial.setValue(200)
        self.orange_dial.setRange(0, 1000)

        self.colors_freqs = {
                        "#13bc15": self.green_dial.value(), 
                        "#efefef": self.white_dial.value(), 
                        "#0000ff": self.blue_dial.value(), 
                        "#ff0000": self.red_dial.value(), 
                        "#d5cd00": self.yellow_dial.value(), 
                        "#ff8a00": self.orange_dial.value(),
                        "#5b5b5b": 0
                        }
        self.synthesizer = Synthesizer()

    def move_cube(self, move_type):
        if (move_type == 'FRONT'):
            self.my_cube.move_F()
        if (move_type == 'RIGHT'):
            self.my_cube.move_R()
        if (move_type == 'right'):
            self.my_cube.move_r()
        if (move_type == 'LEFT'):
            self.my_cube.move_L()
        if (move_type == 'left'):
            self.my_cube.move_l()
        if (move_type == 'UP'):
            self.my_cube.move_U()
        if (move_type == 'up'):
            self.my_cube.move_u()
        if (move_type == 'front'):
            self.my_cube.move_f()

        self.update_tiles()

    # update the color of every tile
    def update_tiles(self):
        for i, face in enumerate(self.gui_cube):
            for j, row in enumerate(face):
                for k, elem in enumerate(row):
                    if (self.tile_on[i, j, k] == True):
                        new_color = self.my_cube.get_sticker(i, j, k).color
                    elif(self.tile_on[i, j, k] == False):
                        new_color = self.tile_off_color
                    elem.setStyleSheet(f"background-color: {new_color}")

    
    # Get the name of the clicked button 
    # use the name to get the indices
    def left_click_tial(self):
        button_name = self.sender().objectName()
        i = self.face_num.get(button_name[0], None)
        j, k = int(button_name[-2:][0]), int(button_name[-2:][1])
        if (self.choosing):
            # show corner label to indicate the button is chosen
            self.label_gui_cube[i][j][k].setAutoFillBackground(True)
            self.sequence_indices.append([i, j, k])
        
    def right_click_tial(self):
        # get indices from button name
        button_name = self.sender().objectName()
        i = self.face_num.get(button_name[0], None)
        j, k = int(button_name[-2:][0]), int(button_name[-2:][1])
        
        if (self.tile_on[i, j, k] == True):
            self.tile_on[i, j, k] = False
            self.update_tiles()
        elif(self.tile_on[i, j, k] == False):
            self.tile_on[i, j, k] = True
            self.update_tiles()

    def choose_sequence(self):
        self.sequence_indices = []
        self.choose.setStyleSheet(f"background-color: {self.toggled_color}")
        self.run.setStyleSheet(f"background-color: {self.untoggled_color}")
        self.choosing = True

    def startRunThread(self):
        self.choosing = False
        self.choose.setStyleSheet(f"background-color: {self.untoggled_color}")
        if len(self.sequence_indices) == 0:
            return
        else:
            self.run.setStyleSheet(f"background-color: {self.toggled_color}")
        # Create a thread and target it to your function
        thread = threading.Thread(target=self.run_sequence)
        # Start the thread
        thread.start()

    def run_sequence(self):
        # loop and play sounds based on indices
        while (self.stopping == False):
            for indices in self.sequence_indices:
                if (self.stopping == True):
                    break
                i = indices[0]
                j = indices[1]
                k = indices[2]

                self.label_gui_cube[i][j][k].setAutoFillBackground(False)

                color = self.gui_cube[i][j][k].palette().color(self.gui_cube[i][j][k].backgroundRole()).name()

                if (color == "#13bc15"): 
                    freq = self.green_dial.value()
                if (color == "#efefef"): 
                    freq = self.white_dial.value()
                if (color == "#0000ff"): 
                    freq = self.blue_dial.value()
                if(color == "#ff0000"): 
                    freq = self.red_dial.value()
                if (color == "#d5cd00"): 
                    freq = self.yellow_dial.value()
                if (color == "#ff8a00"): 
                    freq = self.orange_dial.value()
                if (color =="#5b5b5b"): 
                    freq = 0

                if (freq != 0):
                    self.synthesizer.play_sound(freq)

                time.sleep( 60 / self.tempo_dial.value())
                self.label_gui_cube[i][j][k].setAutoFillBackground(True)
        self.stopping = False

        
    def stop_sequence(self):
        self.run.setStyleSheet(f"background-color: {self.untoggled_color}")
        self.stopping = True
    


def main():
    app = QApplication([])
    window = SequencerGUI()
    app.exec_()

if __name__ == '__main__':
    main()