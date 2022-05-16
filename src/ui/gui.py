from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QLabel

from menu_window import MenuWindow


class GUI(QtWidgets.QMainWindow):
    """
    This is the base window where all the child widgets are placed.
    All the child widgets act as seperate window.
    This also holds all the variables shared with the child widgets
    """

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.image_height = 520
        self.image_width = 920
        self.image_path_not_annotated = "../../images/not_annotated/" # Here you want to move the images you want to annotate
        self.image_path_annotated = "../../images/annotated/"

        self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
        self.horizontal = QtWidgets.QHBoxLayout() # Horizontal main layout
        self.centralWidget().setLayout(self.horizontal)
        self.init_window()

        
    def init_window(self):
        """
        Sets up the window and displays the menu widget.
        """

        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle("Joni's sick annotation program")
        self.show()

        # When started show the Menu widget
        self.curr_widget = MenuWindow(self)
        self.setCentralWidget(self.curr_widget)
